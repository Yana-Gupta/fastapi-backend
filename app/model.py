from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from datetime import datetime



from schema import Roles
from database import Base



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Roles), default="user")
    # createdAt = Column(datetime, default=datetime.now())



class diet(Base):
    __tablename__ = "diet"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(Integer, ForeignKey("users.email"))
    name = Column(String)
    description = Column(String)
    calories = Column(Integer)
    # createdAt = Column(datetime, default=datetime.now())
    # updatedAt = Column(datetime, default=datetime.now())