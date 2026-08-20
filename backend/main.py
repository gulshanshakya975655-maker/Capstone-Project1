
import time
import re
import os
import secrets

from datetime import datetime, timedelta, timezone

import jwt

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from pydantic import BaseModel, Field, field_validator, ValidationError

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from pwdlib import PasswordHash

from backend import algorithms
from backend import models
from backend import schemas

from backend.database import Base, engine, get_db


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# DATABASE MIGRATION
# =========================================================
# Adds new columns to an existing SQLite database.
# This is needed because create_all() does not modify
# an already-existing table.
# =========================================================

def run_database_migrations():
    try:
        with engine.begin() as connection:

            # Check existing users columns
            result = connection.execute(
                text("PRAGMA table_info(users)")
            )

            columns = {
                row[1]
                for row in result.fetchall()
            }

            # Add phone column
            if "phone" not in columns:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN phone VARCHAR"
                    )
                )

            # Add reset token column
            if "reset_token" not in columns:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN reset_token VARCHAR"
                    )
                )

            # Add reset token expiry column
            if "reset_token_expires" not in columns:
                connection.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN reset_token_expires VARCHAR"
                    )
                )

        print("Database migration check completed.")

    except Exception as error:
        print(
            "Database migration warning:",
            error
        )


run_database_migrations()


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="TaskFlow API",
    description="Task and Project Management Platform",
    version="3.0.0",
)


# =========================================================
# AUTHENTICATION CONFIGURATION
# =========================================================

SECRET_KEY = os.getenv(
    "TASKFLOW_SECRET_KEY",
    "taskflow-development-secret-change-me"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

RESET_TOKEN_EXPIRE_MINUTES = 15

password_hash = PasswordHash.recommended()

bearer_scheme = HTTPBearer()


# =========================================================
# PASSWORD FUNCTIONS
# =========================================================

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# ACCESS TOKEN
# =========================================================

def create_access_token(user_id: int) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================================================
# RESET TOKEN
# =========================================================

def create_reset_token() -> str:
    return secrets.token_urlsafe(32)


def get_reset_expiry() -> str:

    expiry = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=RESET_TOKEN_EXPIRE_MINUTES
        )
    )

    return expiry.isoformat()


def reset_token_is_valid(user) -> bool:

    if not user.reset_token:
        return False

    if not user.reset_token_expires:
        return False

    try:

        expiry = datetime.fromisoformat(
            user.reset_token_expires
        )

        if expiry.tzinfo is None:
            expiry = expiry.replace(
                tzinfo=timezone.utc
            )

        return (
            datetime.now(timezone.utc)
            < expiry
        )

    except ValueError:
        return False


# =========================================================
# CUSTOM MIDDLEWARE
# =========================================================

@app.middleware("http")
async def request_timer_middleware(
    request: Request,
    call_next
):

    start = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    response.headers[
        "X-Process-Time-Ms"
    ] = f"{elapsed_ms:.2f}"

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"- {response.status_code} "
        f"- {elapsed_ms:.2f} ms"
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
        "message": "TaskFlow API is running!",
        "version": "3.0.0"
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
        .filter(
            models.Project.id
            == task.project_id
        )
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

def build_quick_add_prompt(
    description: str
):

    return {
        "system": (
            "You are TaskFlow's task parser. "
            "Convert a free-text description "
            "into title, priority and due_date_hint. "
            "Priority must be low, medium, or high."
        ),
        "user": description,
    }


# =========================================================
# QUICK ADD MOCK PARSER
# =========================================================

def parse_quick_add(
    description: str
):

    original = description or ""

    lower_text = original.lower()

    # -----------------------------------------------------
    # PRIORITY
    # -----------------------------------------------------

    if (
        "urgent" in lower_text
        or "asap" in lower_text
    ):

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

        pattern = (
            r"\b"
            + re.escape(phrase)
            + r"\b"
        )

        if re.search(
            pattern,
            lower_text
        ):

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
            r"\b"
            + re.escape(phrase)
            + r"\b",
            "",
            title,
            flags=re.IGNORECASE,
        )


    # Remove date phrase

    if due_date_hint:

        title = re.sub(
            r"\b"
            + re.escape(due_date_hint)
            + r"\b",
            "",
            title,
            flags=re.IGNORECASE,
        )


    # -----------------------------------------------------
    # CLEAN TITLE
    # -----------------------------------------------------

    title = re.sub(
        r"\s+",
        " ",
        title,
    ).strip()

    title = re.sub(
        r"\s+([,.;!?])",
        r"\1",
        title,
    )

    title = title.strip(
        " ,.;!?"
    )

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

    prompt = build_quick_add_prompt(
        data.description
    )

    _ = prompt

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id
            == data.project_id
        )
        .first()
    )

    if not project:

        raise HTTPException(
            status_code=422,
            detail="Project not found",
        )

    parsed = parse_quick_add(
        data.description
    )

    try:

        validated_task = schemas.TaskCreate(

            title=parsed["title"],

            priority=parsed["priority"],

            due_date=parsed[
                "due_date_hint"
            ],

            status="pending",

            project_id=data.project_id,
        )

    except ValidationError as exc:

        raise HTTPException(
            status_code=422,
            detail=exc.errors(),
        )


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
    response_model=list[
        schemas.TaskResponse
    ],
)
def get_tasks(
    sort: str | None = None,
    db: Session = Depends(get_db),
):

    tasks = (
        db.query(models.Task)
        .all()
    )

    if sort is None:

        return tasks


    # -----------------------------------------------------
    # PRIORITY SORT
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

                "priority_rank":
                    priority_rank.get(
                        task.priority,
                        2
                    ),

                "due_date": task.due_date,
                "status": task.status,
                "project_id":
                    task.project_id,
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
                "priority":
                    record["priority"],
                "due_date":
                    record["due_date"],
                "status":
                    record["status"],
                "project_id":
                    record["project_id"],
            }

            for record in records
        ]


    # -----------------------------------------------------
    # DUE DATE SORT
    # -----------------------------------------------------

    if sort == "due_date":

        records = [

            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,

                "due_date":
                    task.due_date or "",

                "status": task.status,

                "project_id":
                    task.project_id,
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
        detail=(
            "sort must be "
            "'priority' or 'due_date'"
        ),
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

    tasks = (
        db.query(models.Task)
        .all()
    )

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

        result = (
            algorithms.linear_search_count(
                records,
                title,
                "title",
            )
        )


    # -----------------------------------------------------
    # BINARY SEARCH
    # -----------------------------------------------------

    elif algo == "binary":

        algorithms.insertion_sort(
            records,
            "title",
        )

        result = (
            algorithms.binary_search_count(
                records,
                title,
                "title",
            )
        )


    else:

        raise HTTPException(
            status_code=400,
            detail=(
                "algo must be "
                "'binary' or 'linear'"
            ),
        )


    index = result["index"]

    comparison_count = (
        result["comparison_count"]
    )


    if index == -1:

        return {

            "algorithm": algo,

            "query": title,

            "found": False,

            "index": -1,

            "comparison_count":
                comparison_count,

            "task": None,
        }


    task_id = (
        records[index]["id"]
    )

    task = (
        db.query(models.Task)
        .filter(
            models.Task.id
            == task_id
        )
        .first()
    )


    if not task:

        return {

            "algorithm": algo,

            "query": title,

            "found": False,

            "index": -1,

            "comparison_count":
                comparison_count,

            "task": None,
        }


    return {

        "algorithm": algo,

        "query": title,

        "found": True,

        "index": index,

        "comparison_count":
            comparison_count,

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
        .filter(
            models.Task.id
            == task_id
        )
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
        .filter(
            models.Task.id
            == task_id
        )
        .first()
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )


    update_data = (
        task_data.model_dump(
            exclude_unset=True
        )
    )


    if "project_id" in update_data:

        project = (
            db.query(models.Project)
            .filter(
                models.Project.id
                == update_data[
                    "project_id"
                ]
            )
            .first()
        )

        if not project:

            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )


    for key, value in update_data.items():

        setattr(
            task,
            key,
            value
        )


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
        .filter(
            models.Task.id
            == task_id
        )
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
        "message":
            "Task deleted successfully"
    }


# =========================================================
# AUTH - REGISTER
# =========================================================

@app.post(
    "/auth/register",
    response_model=schemas.TokenResponse,
    status_code=201,
)
def register(
    user_data: schemas.RegisterRequest,
    db: Session = Depends(get_db),
):

    email = (
        user_data.email
        .strip()
        .lower()
    )

    phone = (
        user_data.phone.strip()
        if user_data.phone
        else None
    )


    # -----------------------------------------------------
    # CHECK EMAIL
    # -----------------------------------------------------

    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email
            == email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )


    # -----------------------------------------------------
    # CHECK PHONE
    # -----------------------------------------------------

    if phone:

        existing_phone = (
            db.query(models.User)
            .filter(
                models.User.phone
                == phone
            )
            .first()
        )

        if existing_phone:

            raise HTTPException(
                status_code=409,
                detail=(
                    "Phone number "
                    "already registered"
                ),
            )


    # -----------------------------------------------------
    # CREATE USER
    # -----------------------------------------------------

    new_user = models.User(

        name=user_data.name.strip(),

        email=email,

        phone=phone,

        password_hash=
            hash_password(
                user_data.password
            ),
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    access_token = (
        create_access_token(
            new_user.id
        )
    )


    return {

        "access_token":
            access_token,

        "token_type":
            "bearer",
    }


# =========================================================
# AUTH - LOGIN
# =========================================================

@app.post(
    "/auth/login",
    response_model=schemas.TokenResponse,
)
def login(
    user_data: schemas.LoginRequest,
    db: Session = Depends(get_db),
):

    email = (
        user_data.email
        .strip()
        .lower()
    )


    user = (
        db.query(models.User)
        .filter(
            models.User.email
            == email
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email "
                "or password"
            ),
        )


    if not user.password_hash:

        raise HTTPException(
            status_code=401,
            detail=(
                "This account does not "
                "have a password. "
                "Please register a new "
                "account."
            ),
        )


    if not verify_password(
        user_data.password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email "
                "or password"
            ),
        )


    access_token = (
        create_access_token(
            user.id
        )
    )


    return {

        "access_token":
            access_token,

        "token_type":
            "bearer",
    }


# =========================================================
# AUTH - FORGOT PASSWORD
# =========================================================

@app.post(
    "/auth/forgot-password"
)
def forgot_password(
    request_data:
        schemas.ForgotPasswordRequest,

    db: Session =
        Depends(get_db),
):

    email = (
        request_data.email.strip().lower()
        if request_data.email
        else None
    )

    phone = (
        request_data.phone.strip()
        if request_data.phone
        else None
    )


    if not email and not phone:

        raise HTTPException(
            status_code=422,
            detail=(
                "Please provide "
                "email or phone number"
            ),
        )


    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    query = db.query(models.User)


    if email:

        user = (
            query
            .filter(
                models.User.email
                == email
            )
            .first()
        )

    else:

        user = (
            query
            .filter(
                models.User.phone
                == phone
            )
            .first()
        )


    # -----------------------------------------------------
    # USER NOT FOUND
    # -----------------------------------------------------

    if not user:

        raise HTTPException(
            status_code=404,
            detail=(
                "No TaskFlow account "
                "was found with this "
                "email or phone number."
            ),
        )


    # -----------------------------------------------------
    # CREATE RESET TOKEN
    # -----------------------------------------------------

    reset_token = (
        create_reset_token()
    )

    reset_expiry = (
        get_reset_expiry()
    )


    user.reset_token = reset_token

    user.reset_token_expires = (
        reset_expiry
    )


    db.commit()

    db.refresh(user)


    # -----------------------------------------------------
    # DEVELOPMENT RESET LINK
    # -----------------------------------------------------
    # Real email sending will be connected later.
    # For now, the link is returned so we can test
    # the complete reset-password flow.
    # -----------------------------------------------------

    # reset_link = (
    #     "http://127.0.0.1:5500/frontend/"
    #     "reset-password.html"
    #     "?token="
    #     + reset_token
    # )

    reset_link = (
    "https://capstone-project1-ovg9.onrender.com/"
    "reset-password.html"
    "?token="
    + reset_token
)


    print(
        "\n================================="
    )

    print(
        "TASKFLOW PASSWORD RESET"
    )

    print(
        "User:",
        user.email
    )

    print(
        "Reset link:",
        reset_link
    )

    print(
        "=================================\n"
    )


    return {

        "message": (
            "Password reset link "
            "generated successfully."
        ),

        "reset_link":
            reset_link,

        "expires_in_minutes":
            RESET_TOKEN_EXPIRE_MINUTES,
    }


# =========================================================
# AUTH - RESET PASSWORD
# =========================================================

@app.post(
    "/auth/reset-password",
    response_model=
        schemas.PasswordResetResponse,
)
def reset_password(
    request_data:
        schemas.ResetPasswordRequest,

    db: Session =
        Depends(get_db),
):

    token = (
        request_data.token.strip()
    )


    # -----------------------------------------------------
    # FIND USER BY RESET TOKEN
    # -----------------------------------------------------

    user = (
        db.query(models.User)
        .filter(
            models.User.reset_token
            == token
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid or expired "
                "password reset token."
            ),
        )


    # -----------------------------------------------------
    # CHECK TOKEN EXPIRY
    # -----------------------------------------------------

    if not reset_token_is_valid(user):

        user.reset_token = None

        user.reset_token_expires = None

        db.commit()


        raise HTTPException(
            status_code=400,
            detail=(
                "This password reset "
                "link has expired."
            ),
        )


    # -----------------------------------------------------
    # CHANGE PASSWORD
    # -----------------------------------------------------

    user.password_hash = (
        hash_password(
            request_data.new_password
        )
    )


    # -----------------------------------------------------
    # DELETE USED TOKEN
    # -----------------------------------------------------

    user.reset_token = None

    user.reset_token_expires = None


    db.commit()

    db.refresh(user)


    return {

        "message": (
            "Password reset successfully. "
            "You can now login with your "
            "new password."
        )
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

    email = (
        user.email
        .strip()
        .lower()
    )

    phone = (
        user.phone.strip()
        if user.phone
        else None
    )


    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email
            == email
        )
        .first()
    )


    if existing_user:

        raise HTTPException(
            status_code=422,
            detail="Email already exists",
        )


    if phone:

        existing_phone = (
            db.query(models.User)
            .filter(
                models.User.phone
                == phone
            )
            .first()
        )

        if existing_phone:

            raise HTTPException(
                status_code=422,
                detail=(
                    "Phone number "
                    "already exists"
                ),
            )


    new_user = models.User(

        name=user.name.strip(),

        email=email,

        phone=phone,
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
    response_model=list[
        schemas.UserResponse
    ],
)
def get_users(
    db: Session = Depends(get_db),
):

    return (
        db.query(models.User)
        .all()
    )


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
        .filter(
            models.User.id
            == user_id
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )


    email = (
        user_data.email
        .strip()
        .lower()
    )


    phone = (
        user_data.phone.strip()
        if user_data.phone
        else None
    )


    duplicate = (
        db.query(models.User)
        .filter(
            models.User.email
            == email,

            models.User.id
            != user_id,
        )
        .first()
    )


    if duplicate:

        raise HTTPException(
            status_code=422,
            detail="Email already exists",
        )


    if phone:

        duplicate_phone = (
            db.query(models.User)
            .filter(
                models.User.phone
                == phone,

                models.User.id
                != user_id,
            )
            .first()
        )

        if duplicate_phone:

            raise HTTPException(
                status_code=422,
                detail=(
                    "Phone number "
                    "already exists"
                ),
            )


    user.name = (
        user_data.name.strip()
    )

    user.email = email

    user.phone = phone


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
        .filter(
            models.User.id
            == user_id
        )
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
        "message":
            "User deleted successfully"
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
            models.User.id
            == project.owner_id
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
    response_model=list[
        schemas.ProjectResponse
    ],
)
def get_projects(
    db: Session = Depends(get_db),
):

    return (
        db.query(models.Project)
        .all()
    )


# =========================================================
# PROJECT STATISTICS
# =========================================================

@app.get(
    "/projects/{project_id}/stats"
)
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
):

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id
            == project_id
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
            ).label(
                "task_count"
            ),
        )

        .outerjoin(

            models.Task,

            models.Task.project_id
            == models.Project.id,
        )

        .filter(

            models.Project.id
            == project_id
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

        "project_id":
            project_id,

        "total":
            total,

        "pending":
            pending,

        "completed":
            completed,
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
            models.Project.id
            == project_id
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


    project.name = (
        project_data.name
    )

    project.owner_id = (
        project_data.owner_id
    )


    db.commit()

    db.refresh(project)


    return project


# =========================================================
# PROJECT DELETE
# =========================================================

@app.delete(
    "/projects/{project_id}"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id
            == project_id
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
        "message":
            "Project deleted successfully"
    }


# =========================================================
# ALGORITHM - INSERTION SORT
# =========================================================

@app.post(
    "/algorithms/sort"
)
def sort_numbers(
    numbers: list[int],
):

    records = [

        {
            "value": number
        }

        for number in numbers
    ]


    algorithms.insertion_sort(
        records,
        "value",
    )


    return {

        "algorithm":
            "insertion_sort",

        "input":
            numbers,

        "sorted": [

            record["value"]

            for record in records
        ],
    }


# =========================================================
# ALGORITHM - LINEAR SEARCH
# =========================================================

@app.get(
    "/algorithms/linear-search"
)
def search_linear(
    numbers: str,
    target: int,
):

    try:

        number_list = [

            int(number.strip())

            for number
            in numbers.split(",")

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

        {
            "value": number
        }

        for number in number_list
    ]


    index = algorithms.linear_search(

        records,

        target,

        "value",
    )


    return {

        "algorithm":
            "linear_search",

        "numbers":
            number_list,

        "target":
            target,

        "index":
            index,
    }


# =========================================================
# ALGORITHM - BINARY SEARCH
# =========================================================

@app.get(
    "/algorithms/binary-search"
)
def search_binary(
    numbers: str,
    target: int,
):

    try:

        number_list = [

            int(number.strip())

            for number
            in numbers.split(",")

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

        {
            "value": number
        }

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

        "algorithm":
            "binary_search",

        "numbers": [

            record["value"]

            for record in records
        ],

        "target":
            target,

        "index":
            index,
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

@app.post(
    "/algorithms/benchmark"
)
def benchmark_algorithms(
    data: BenchmarkRequest,
):

    original_numbers = list(
        data.numbers
    )


    # -----------------------------------------------------
    # INSERTION SORT
    # -----------------------------------------------------

    sort_records = [

        {
            "value": number
        }

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
    # LINEAR SEARCH
    # -----------------------------------------------------

    linear_records = [

        {
            "value": number
        }

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
    # BINARY SEARCH
    # -----------------------------------------------------

    binary_result = (
        algorithms.binary_search_count(

            sort_records,

            data.target,

            "value",
        )
    )


    return {

        "input":
            original_numbers,

        "target":
            data.target,

        "sorted_numbers":
            sorted_numbers,


        "insertion_sort": {

            "comparisons":
                sort_comparisons,
        },


        "linear_search": {

            "index":
                linear_result["index"],

            "comparisons":
                linear_result[
                    "comparison_count"
                ],
        },


        "binary_search": {

            "index":
                binary_result["index"],

            "comparisons":
                binary_result[
                    "comparison_count"
                ],
        },
    }
