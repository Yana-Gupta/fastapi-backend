from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime
from datetime import datetime


from schema import Roles
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Roles), default="user")
    createdAt = Column(DateTime, default=datetime.now())



class Diet(Base):
    __tablename__ = "diet"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(Integer, ForeignKey("users.email"))
    name = Column(String)
    description = Column(String)
    calories = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())
    # updatedAt = Column(datetime, default=datetime.now())