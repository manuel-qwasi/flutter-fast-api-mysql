from pydantic import BaseModel, EmailStr
from typing import Optional


# Shared base schema for User (used in multiple places)
class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    phone: Optional[str] = None  # Phone is optional
    email: EmailStr # Email validation
    is_vendor : bool = False # Default is False


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for creating a new user (includes password)
class UserCreate(UserBase):
    password: str # Accepts raw password input

# Schema for returning user data (does NOT include password)
class UserResponse(UserBase):
    id: int # Add ID to response

    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy model to Pydantic model
