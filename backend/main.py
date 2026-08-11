import time
import re
from datetime import date, timedelta

import algorithms

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import Base, engine, get_db
import models
import schemas


# ==========================================
# DATABASE
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(
    title="TaskFlow API",
    description="Task and Project Management Platform",
    version="1.0.0"
)


# ==========================================
# REQUEST TIME MIDDLEWARE
# ==========================================

@app.middleware("http")
async def request_timer_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    print(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} "
        f"- {process_time:.6f}s"
    )

    return response


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "message": "TaskFlow API is running!"
    }


# ==========================================
# CREATE TASK
# ==========================================

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        status=task.status,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ==========================================
# AI QUICK-ADD
# ==========================================

class QuickAddRequest(BaseModel):
    description: str
    project_id: int


def parse_quick_add(description: str):
    """
    Deterministic natural-language parser.

    Rules:
    - urgent / asap -> high priority
    - low priority / low -> low priority
    - otherwise -> medium priority
    - today -> today's date
    - tomorrow -> tomorrow's date
    - next week -> 7 days from today
    - otherwise -> no due date
    - title = cleaned description
    """

    text = description.strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Description cannot be empty"
        )

    lower_text = text.lower()

    # --------------------------------------
    # PRIORITY
    # --------------------------------------

    if (
        "urgent" in lower_text
        or "asap" in lower_text
        or "high priority" in lower_text
    ):
        priority = "high"

    elif (
        "low priority" in lower_text
        or re.search(r"\blow\b", lower_text)
    ):
        priority = "low"

    else:
        priority = "medium"

    # --------------------------------------
    # DUE DATE
    # --------------------------------------

    due_date = None

    if "tomorrow" in lower_text:
        due_date = date.today() + timedelta(days=1)

    elif "today" in lower_text:
        due_date = date.today()

    elif "next week" in lower_text:
        due_date = date.today() + timedelta(days=7)

    # --------------------------------------
    # EXPLICIT DATE: YYYY-MM-DD
    # --------------------------------------

    date_match = re.search(
        r"\b(20\d{2})-(\d{2})-(\d{2})\b",
        text
    )

    if date_match:
        try:
            due_date = date(
                int(date_match.group(1)),
                int(date_match.group(2)),
                int(date_match.group(3))
            )
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid date"
            )

    # --------------------------------------
    # CLEAN TITLE
    # --------------------------------------

    title = text

    remove_phrases = [
        "urgent",
        "asap",
        "high priority",
        "low priority",
        "today",
        "tomorrow",
        "next week"
    ]

    for phrase in remove_phrases:
        title = re.sub(
            re.escape(phrase),
            "",
            title,
            flags=re.IGNORECASE
        )

    title = re.sub(
        r"\b20\d{2}-\d{2}-\d{2}\b",
        "",
        title
    )

    title = re.sub(r"\s+", " ", title)
    title = title.strip(" ,.-")

    if not title:
        title = text

    return {
        "title": title,
        "priority": priority,
        "due_date": due_date
    }


@app.post(
    "/tasks/quick-add",
    response_model=schemas.TaskResponse,
    status_code=201
)
def quick_add_task(
    data: QuickAddRequest,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == data.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    parsed = parse_quick_add(data.description)

    new_task = models.Task(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date"],
        status="pending",
        project_id=data.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ==========================================
# LIST TASKS
# ==========================================

@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).all()

    # --------------------------------------
    # INSERTION SORT BY PRIORITY
    # --------------------------------------

    if sort == "priority":

        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        for i in range(1, len(tasks)):
            key = tasks[i]
            key_priority = priority_order.get(
                key.priority,
                2
            )

            j = i - 1

            while j >= 0:
                current_priority = priority_order.get(
                    tasks[j].priority,
                    2
                )

                if current_priority > key_priority:
                    tasks[j + 1] = tasks[j]
                    j -= 1
                else:
                    break

            tasks[j + 1] = key

    # --------------------------------------
    # SORT BY DUE DATE
    # --------------------------------------

    elif sort == "due_date":

        tasks.sort(
            key=lambda task: (
                task.due_date is None,
                task.due_date or date.max
            )
        )

    return tasks


# ==========================================
# SEARCH TASKS
# ==========================================

@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = "linear",
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).all()

    titles = [
        task.title
        for task in tasks
    ]

    if algo == "linear":

        index, comparisons = (
            algorithms.linear_search_with_comparisons(
                titles,
                title
            )
        )

        task = (
            tasks[index]
            if index != -1
            else None
        )

        return {
            "algorithm": "linear",
            "target": title,
            "found": index != -1,
            "index": index,
            "comparisons": comparisons,
            "task": task
        }

    elif algo == "binary":

        sorted_pairs = sorted(
            enumerate(titles),
            key=lambda item: item[1].lower()
        )

        sorted_titles = [
            title_value
            for _, title_value in sorted_pairs
        ]

        index, comparisons = (
            algorithms.binary_search_with_comparisons(
                sorted_titles,
                title
            )
        )

        original_index = -1

        if index != -1:
            original_index = sorted_pairs[index][0]

        task = (
            tasks[original_index]
            if original_index != -1
            else None
        )

        return {
            "algorithm": "binary",
            "target": title,
            "found": original_index != -1,
            "index": original_index,
            "comparisons": comparisons,
            "task": task
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="algo must be 'linear' or 'binary'"
        )


# ==========================================
# GET TASK
# ==========================================

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# ==========================================
# UPDATE TASK
# ==========================================

@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# ==========================================
# DELETE TASK
# ==========================================

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# ==========================================
# CREATE USER
# ==========================================

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=201
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=422,
            detail="Email already exists"
        )

    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==========================================
# LIST USERS
# ==========================================

@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(models.User).all()


# ==========================================
# UPDATE USER
# ==========================================

@app.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)
def update_user(
    user_id: int,
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email,
        models.User.id != user_id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=422,
            detail="Email already exists"
        )

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


# ==========================================
# DELETE USER
# ==========================================

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }


# ==========================================
# CREATE PROJECT
# ==========================================

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=201
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = db.query(models.User).filter(
        models.User.id == project.owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# ==========================================
# LIST PROJECTS
# ==========================================

@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):
    return db.query(models.Project).all()


# ==========================================
# PROJECT STATISTICS
# ==========================================

@app.get("/projects/{project_id}/stats")
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    stats = db.query(
        models.Task.status,
        func.count(models.Task.id)
    ).filter(
        models.Task.project_id == project_id
    ).group_by(
        models.Task.status
    ).all()

    counts = {
        "pending": 0,
        "completed": 0
    }

    for status, count in stats:
        if status in counts:
            counts[status] = count

    total = sum(counts.values())

    return {
        "project_id": project_id,
        "total": total,
        "pending": counts["pending"],
        "completed": counts["completed"]
    }


# ==========================================
# UPDATE PROJECT
# ==========================================

@app.put(
    "/projects/{project_id}",
    response_model=schemas.ProjectResponse
)
def update_project(
    project_id: int,
    project_data: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    owner = db.query(models.User).filter(
        models.User.id == project_data.owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project.name = project_data.name
    project.owner_id = project_data.owner_id

    db.commit()
    db.refresh(project)

    return project


# ==========================================
# DELETE PROJECT
# ==========================================

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }


# ==========================================
# ALGORITHMS - INSERTION SORT
# ==========================================

@app.post("/algorithms/sort")
def sort_numbers(numbers: list[int]):
    return {
        "algorithm": "insertion_sort",
        "input": numbers,
        "sorted": algorithms.insertion_sort(numbers)
    }


# ==========================================
# LINEAR SEARCH
# ==========================================

@app.get("/algorithms/linear-search")
def search_linear(
    numbers: str,
    target: int
):
    try:
        number_list = [
            int(number.strip())
            for number in numbers.split(",")
        ]
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="numbers must contain comma-separated integers"
        )

    index = algorithms.linear_search(
        number_list,
        target
    )

    return {
        "algorithm": "linear_search",
        "numbers": number_list,
        "target": target,
        "index": index
    }


# ==========================================
# BINARY SEARCH
# ==========================================

@app.get("/algorithms/binary-search")
def search_binary(
    numbers: str,
    target: int
):
    try:
        number_list = [
            int(number.strip())
            for number in numbers.split(",")
        ]
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="numbers must contain comma-separated integers"
        )

    number_list = algorithms.insertion_sort(
        number_list
    )

    index = algorithms.binary_search(
        number_list,
        target
    )

    return {
        "algorithm": "binary_search",
        "numbers": number_list,
        "target": target,
        "index": index
    }


# ==========================================
# ALGORITHM BENCHMARK
# ==========================================

class BenchmarkRequest(BaseModel):
    numbers: list[int]
    target: int


@app.post("/algorithms/benchmark")
def benchmark_algorithms(
    data: BenchmarkRequest
):
    numbers = data.numbers
    target = data.target

    sorted_numbers, sort_comparisons = (
        algorithms.insertion_sort_with_comparisons(
            numbers
        )
    )

    linear_index, linear_comparisons = (
        algorithms.linear_search_with_comparisons(
            numbers,
            target
        )
    )

    binary_index, binary_comparisons = (
        algorithms.binary_search_with_comparisons(
            sorted_numbers,
            target
        )
    )

    return {
        "input": numbers,
        "target": target,
        "sorted_numbers": sorted_numbers,
        "insertion_sort": {
            "comparisons": sort_comparisons
        },
        "linear_search": {
            "index": linear_index,
            "comparisons": linear_comparisons
        },
        "binary_search": {
            "index": binary_index,
            "comparisons": binary_comparisons
        }
    }