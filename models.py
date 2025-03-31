from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(15), unique=True, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), unique=True, nullable=False)
    is_vendor = Column(Boolean, default=False)

