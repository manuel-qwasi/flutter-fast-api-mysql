from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models, schemas


pwd_context = CryptContext(schemas=["bcrypt"], depecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashed_password(user.password)
    db_user = models.User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        is_vendor=user.is_vendor
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get latest DB state
    return db_user

def get_user_by_id(db:Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# READ: Get a user by email (for login)
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# READ: Get a user by phone (for login)
def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()

# READ: Get a user by username (for login)
def get_user_by_phone(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
