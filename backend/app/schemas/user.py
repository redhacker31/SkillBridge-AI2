from datetime import datetime
import re
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class UserBase(BaseModel):
    email: str
    full_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Invalid email format")
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None
