import time
import re

from backend import algorithms
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import Base, engine, get_db
from backend import models
from backend import schemas


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="TaskFlow API",
    description="Task and Project Management Platform",
    version="2.0.0",
)


# =========================================================
# CUSTOM MIDDLEWARE
# =========================================================

@app.middleware("http")
async def request_timer_middleware(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start) * 1000

    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"

    print(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} - {elapsed_ms:.2f} ms"
    )

    return response


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "TaskFlow API is running!"
    }


# =========================================================
# TASK CREATE
# =========================================================

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201,
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == task.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    new_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        status=task.status,
        project_id=task.project_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# =========================================================
# QUICK ADD REQUEST
# =========================================================

class QuickAddRequest(BaseModel):
    description: str
    project_id: int

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if not value or not value.strip():
            raise ValueError(
                "description cannot be blank"
            )

        return value.strip()


# =========================================================
# QUICK ADD PROMPT
# =========================================================

def build_quick_add_prompt(description: str):
    return {
        "system": (
            "You are TaskFlow's task parser. Convert a free-text "
            "description into title, priority and due_date_hint. "
            "Priority must be low, medium, or high."
        ),
        "user": description,
    }


# =========================================================
# QUICK ADD MOCK PARSER
# =========================================================

def parse_quick_add(description: str):
    original = description or ""
    lower_text = original.lower()

    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    if "urgent" in lower_text or "asap" in lower_text:
        priority = "high"

    elif (
        "whenever" in lower_text
        or "low priority" in lower_text
    ):
        priority = "low"

    else:
        priority = "medium"

    # -----------------------------------------------------
    # DUE DATE
    # -----------------------------------------------------

    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    due_date_hint = None

    for phrase in date_phrases:
        pattern = r"\b" + re.escape(phrase) + r"\b"

        if re.search(pattern, lower_text):
            due_date_hint = phrase
            break

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    title = original

    priority_phrases = [
        "urgent",
        "asap",
        "whenever",
        "low priority",
    ]

    for phrase in priority_phrases:
        title = re.sub(
            r"\b" + re.escape(phrase) + r"\b",
            "",
            title,
            flags=re.IGNORECASE,
        )

    if due_date_hint:
        title = re.sub(
            r"\b" + re.escape(due_date_hint) + r"\b",
            "",
            title,
            flags=re.IGNORECASE,
        )

    # -----------------------------------------------------
    # CLEAN TITLE
    # -----------------------------------------------------

    # Convert multiple spaces into one, trim ends
    title = re.sub(r"\s+", " ", title).strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }


# =========================================================
# QUICK ADD ENDPOINT
# =========================================================

@app.post(
    "/tasks/quick-add",
    response_model=schemas.TaskResponse,
    status_code=201,
)
def quick_add_task(
    data: QuickAddRequest,
    db: Session = Depends(get_db),
):
    # Build standard prompt structure
    prompt = build_quick_add_prompt(
        data.description
    )

    # Reserved for future LLM integration
    _ = prompt

    # -----------------------------------------------------
    # PROJECT VALIDATION
    # -----------------------------------------------------

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == data.project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=422,
            detail="Project not found",
        )

    # -----------------------------------------------------
    # MOCK PARSER
    # -----------------------------------------------------

    parsed = parse_quick_add(
        data.description
    )

    # -----------------------------------------------------
    # VALIDATE BEFORE DATABASE WRITE
    # -----------------------------------------------------

    try:
        validated_task = schemas.TaskCreate(
            title=parsed["title"],
            priority=parsed["priority"],
            due_date=parsed["due_date_hint"],
            status="pending",
            project_id=data.project_id,
        )

    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=exc.errors(),
        )

    # -----------------------------------------------------
    # CREATE DATABASE ROW
    # -----------------------------------------------------

    new_task = models.Task(
        title=validated_task.title,
        priority=validated_task.priority,
        due_date=validated_task.due_date,
        status=validated_task.status,
        project_id=validated_task.project_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# =========================================================
# LIST TASKS
# =========================================================

@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse],
)
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    tasks = db.query(models.Task).all()

    # -----------------------------------------------------
    # NORMAL LIST
    # -----------------------------------------------------

    if sort is None:
        return tasks

    # -----------------------------------------------------
    # INSERTION SORT BY PRIORITY
    # -----------------------------------------------------

    if sort == "priority":

        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }

        records = [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "priority_rank": priority_rank.get(
                    task.priority,
                    2,
                ),
                "due_date": task.due_date,
                "status": task.status,
                "project_id": task.project_id,
            }
            for task in tasks
        ]

        algorithms.insertion_sort(
            records,
            "priority_rank",
        )

        return [
            {
                "id": record["id"],
                "title": record["title"],
                "priority": record["priority"],
                "due_date": record["due_date"],
                "status": record["status"],
                "project_id": record["project_id"],
            }
            for record in records
        ]

    # -----------------------------------------------------
    # INSERTION SORT BY DUE DATE
    # -----------------------------------------------------

    if sort == "due_date":

        records = [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date or "",
                "status": task.status,
                "project_id": task.project_id,
            }
            for task in tasks
        ]

        algorithms.insertion_sort(
            records,
            "due_date",
        )

        return records

    raise HTTPException(
        status_code=400,
        detail="sort must be 'priority' or 'due_date'",
    )


# =========================================================
# SEARCH TASKS
# =========================================================

@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db),
):
    tasks = db.query(models.Task).all()

    if not tasks:
        return {
            "algorithm": algo,
            "query": title,
            "found": False,
            "index": -1,
            "comparison_count": 0,
            "task": None,
        }

    records = [
        {
            "id": task.id,
            "title": task.title,
        }
        for task in tasks
    ]

    # -----------------------------------------------------
    # LINEAR SEARCH
    # -----------------------------------------------------

    if algo == "linear":

        result = algorithms.linear_search_count(
            records,
            title,
            "title",
        )

    # -----------------------------------------------------
    # BINARY SEARCH
    # -----------------------------------------------------

    elif algo == "binary":

        algorithms.insertion_sort(
            records,
            "title",
        )

        result = algorithms.binary_search_count(
            records,
            title,
            "title",
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="algo must be 'binary' or 'linear'",
        )

    index = result["index"]
    comparison_count = result["comparison_count"]

    # -----------------------------------------------------
    # NOT FOUND
    # -----------------------------------------------------

    if index == -1:
        return {
            "algorithm": algo,
            "query": title,
            "found": False,
            "index": -1,
            "comparison_count": comparison_count,
            "task": None,
        }

    # -----------------------------------------------------
    # FOUND
    # -----------------------------------------------------

    task_id = records[index]["id"]

    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        return {
            "algorithm": algo,
            "query": title,
            "found": False,
            "index": -1,
            "comparison_count": comparison_count,
            "task": None,
        }

    return {
        "algorithm": algo,
        "query": title,
        "found": True,
        "index": index,
        "comparison_count": comparison_count,
        "task": task,
    }


# =========================================================
# GET SINGLE TASK
# =========================================================

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


# =========================================================
# UPDATE TASK
# =========================================================

@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    if "project_id" in update_data:

        project = (
            db.query(models.Project)
            .filter(
                models.Project.id
                == update_data["project_id"]
            )
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# =========================================================
# DELETE TASK
# =========================================================

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# =========================================================
# USERS - CREATE
# =========================================================

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=201,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email == user.email
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=422,
            detail="Email already exists",
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================================
# USERS - LIST
# =========================================================

@app.get(
    "/users",
    response_model=list[schemas.UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return db.query(models.User).all()


# =========================================================
# USERS - UPDATE
# =========================================================

@app.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
)
def update_user(
    user_id: int,
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    duplicate = (
        db.query(models.User)
        .filter(
            models.User.email == user_data.email,
            models.User.id != user_id,
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=422,
            detail="Email already exists",
        )

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


# =========================================================
# USERS - DELETE
# =========================================================

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }


# =========================================================
# PROJECTS - CREATE
# =========================================================

@app.post(
    "/projects",
    response_model=schemas.ProjectResponse,
    status_code=201,
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    owner = (
        db.query(models.User)
        .filter(
            models.User.id == project.owner_id
        )
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# =========================================================
# PROJECTS - LIST
# =========================================================

@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
):
    return db.query(models.Project).all()


# =========================================================
# PROJECT STATISTICS
# =========================================================

@app.get("/projects/{project_id}/stats")
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    rows = (
        db.query(
            models.Project.id.label(
                "project_id"
            ),
            models.Task.status.label(
                "status"
            ),
            func.count(
                models.Task.id
            ).label("task_count"),
        )
        .outerjoin(
            models.Task,
            models.Task.project_id
            == models.Project.id,
        )
        .filter(
            models.Project.id == project_id
        )
        .group_by(
            models.Project.id,
            models.Task.status,
        )
        .all()
    )

    pending = 0
    completed = 0
    total = 0

    for row in rows:

        count = int(
            row.task_count or 0
        )

        total += count

        if row.status == "pending":
            pending += count

        elif row.status == "completed":
            completed += count

    return {
        "project_id": project_id,
        "total": total,
        "pending": pending,
        "completed": completed,
    }


# =========================================================
# PROJECT UPDATE
# =========================================================

@app.put(
    "/projects/{project_id}",
    response_model=schemas.ProjectResponse,
)
def update_project(
    project_id: int,
    project_data: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    owner = (
        db.query(models.User)
        .filter(
            models.User.id
            == project_data.owner_id
        )
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    project.name = project_data.name
    project.owner_id = project_data.owner_id

    db.commit()
    db.refresh(project)

    return project


# =========================================================
# PROJECT DELETE
# =========================================================

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }


# =========================================================
# ALGORITHM - INSERTION SORT
# =========================================================

@app.post("/algorithms/sort")
def sort_numbers(
    numbers: list[int],
):

    records = [
        {"value": number}
        for number in numbers
    ]

    algorithms.insertion_sort(
        records,
        "value",
    )

    return {
        "algorithm": "insertion_sort",
        "input": numbers,
        "sorted": [
            record["value"]
            for record in records
        ],
    }


# =========================================================
# ALGORITHM - LINEAR SEARCH
# =========================================================

@app.get("/algorithms/linear-search")
def search_linear(
    numbers: str,
    target: int,
):

    try:
        number_list = [
            int(number.strip())
            for number in numbers.split(",")
            if number.strip()
        ]

    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=(
                "numbers must contain "
                "comma-separated integers"
            ),
        )

    records = [
        {"value": number}
        for number in number_list
    ]

    index = algorithms.linear_search(
        records,
        target,
        "value",
    )

    return {
        "algorithm": "linear_search",
        "numbers": number_list,
        "target": target,
        "index": index,
    }


# =========================================================
# ALGORITHM - BINARY SEARCH
# =========================================================

@app.get("/algorithms/binary-search")
def search_binary(
    numbers: str,
    target: int,
):

    try:
        number_list = [
            int(number.strip())
            for number in numbers.split(",")
            if number.strip()
        ]

    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=(
                "numbers must contain "
                "comma-separated integers"
            ),
        )

    records = [
        {"value": number}
        for number in number_list
    ]

    algorithms.insertion_sort(
        records,
        "value",
    )

    index = algorithms.binary_search(
        records,
        target,
        "value",
    )

    return {
        "algorithm": "binary_search",
        "numbers": [
            record["value"]
            for record in records
        ],
        "target": target,
        "index": index,
    }


# =========================================================
# BENCHMARK REQUEST
# =========================================================

class BenchmarkRequest(BaseModel):
    numbers: list[int]
    target: int


# =========================================================
# ALGORITHM BENCHMARK
# =========================================================

@app.post("/algorithms/benchmark")
def benchmark_algorithms(
    data: BenchmarkRequest,
):

    original_numbers = list(
        data.numbers
    )

    # -----------------------------------------------------
    # INSERTION SORT COUNT
    # -----------------------------------------------------

    sort_records = [
        {"value": number}
        for number in original_numbers
    ]

    sort_comparisons = (
        algorithms.insertion_sort_count(
            sort_records,
            "value",
        )
    )

    sorted_numbers = [
        record["value"]
        for record in sort_records
    ]

    # -----------------------------------------------------
    # LINEAR SEARCH COUNT
    # -----------------------------------------------------

    linear_records = [
        {"value": number}
        for number in original_numbers
    ]

    linear_result = (
        algorithms.linear_search_count(
            linear_records,
            data.target,
            "value",
        )
    )

    # -----------------------------------------------------
    # BINARY SEARCH COUNT
    # -----------------------------------------------------

    binary_result = (
        algorithms.binary_search_count(
            sort_records,
            data.target,
            "value",
        )
    )

    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return {
        "input": original_numbers,
        "target": data.target,
        "sorted_numbers": sorted_numbers,

        "insertion_sort": {
            "comparisons": sort_comparisons,
        },

        "linear_search": {
            "index": linear_result["index"],
            "comparisons": linear_result[
                "comparison_count"
            ],
        },

        "binary_search": {
            "index": binary_result["index"],
            "comparisons": binary_result[
                "comparison_count"
            ],
        },
    }