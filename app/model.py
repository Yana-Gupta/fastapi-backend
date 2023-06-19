from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime
from datetime import datetime, date
from app.database import Base
from app.schema import Roles

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    daily_calories = Column(Integer, default=-1)
    role = Column(Enum(Roles), default="user")
    createdAt = Column(DateTime, default=datetime.now())


class Diet(Base):
    __tablename__ = "diet"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(Integer, ForeignKey("users.email"))
    name = Column(String)
    description = Column(String)
    calories = Column(Integer, default=-1)
    isLessThan = Column(Boolean, default=True)
    date= Column(DateTime, default=date.today())
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now())