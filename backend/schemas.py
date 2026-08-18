
from pydantic import BaseModel, Field, field_validator
from typing import Optional


# =========================================================
# TASK SCHEMAS
# =========================================================

class TaskCreate(BaseModel):
    title: str

    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )

    due_date: Optional[str] = None

    status: str = "pending"

    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = None

    priority: Optional[str] = Field(
        default=None,
        pattern="^(low|medium|high)$"
    )

    due_date: Optional[str] = None

    status: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Title cannot be blank")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[str]
    status: str
    project_id: int

    class Config:
        from_attributes = True


# =========================================================
# USER SCHEMAS
# =========================================================

class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be blank")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()

        if not value:
            raise ValueError("Email cannot be blank")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip()

            if value and not value.isdigit():
                raise ValueError(
                    "Phone number must contain only digits"
                )

        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

    class Config:
        from_attributes = True


# =========================================================
# PROJECT SCHEMAS
# =========================================================

class ProjectCreate(BaseModel):
    name: str
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


# =========================================================
# AUTH - REGISTER
# =========================================================

class RegisterRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    password: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be blank")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()

        if not value:
            raise ValueError("Email cannot be blank")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip()

            if value and not value.isdigit():
                raise ValueError(
                    "Phone number must contain only digits"
                )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError(
                "Password must be at least 6 characters"
            )

        return value


# =========================================================
# AUTH - LOGIN
# =========================================================

class LoginRequest(BaseModel):
    email: str
    password: str


# =========================================================
# AUTH - TOKEN
# =========================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================================================
# FORGOT PASSWORD
# =========================================================

class ForgotPasswordRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if value is not None:
            value = value.strip().lower()

            if not value:
                return None

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            value = value.strip()

            if not value:
                return None

            if not value.isdigit():
                raise ValueError(
                    "Phone number must contain only digits"
                )

        return value


# =========================================================
# RESET PASSWORD
# =========================================================

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("token")
    @classmethod
    def validate_token(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Reset token is required")

        return value

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError(
                "Password must be at least 6 characters"
            )

        return value


# =========================================================
# PASSWORD RESET RESPONSE
# =========================================================

class PasswordResetResponse(BaseModel):
    message: str

