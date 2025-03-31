from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

import crud
from database import get_db  # Function to get database session
from schemas import Token, UserLogin, UserCreate, UserResponse  # Pydantic models
from models import User
import schemas  # SQLAlchemy User model

# Load secret keys from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# User registration
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create a new user
    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        phone=user.phone,
        email=user.email,
        password=hashed_password,
        is_vendor=user.is_vendor
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# User login
@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create JWT access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint: Get all users (paginated)
@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Endpoint: Get a user by ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoint: Delete a user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
