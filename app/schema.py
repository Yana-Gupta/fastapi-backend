from enum import Enum
from pydantic import BaseModel


class Roles(str, Enum):
    user = "user"
    admin = "admin"
    user_manager = "user_manager"


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    role: Roles
    name: str
    daily_calories: int


class UserUpdate(UserBase):
    name: str
    daily_calories: int
    pass


class DietBase(BaseModel):
    name: str
    description: str
    calories: int


class DietCreate(DietBase):
    pass
    

class DietUpdate(DietBase):
    pass

class Diet(DietBase):
    email: str
