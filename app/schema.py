from enum import Enum
from pydantic import BaseModel


class Roles(str, Enum):
    user = "user"
    admin = "admin"
    user_manager = "user_manager"



class UserBase(BaseModel):
    name: str
    email: str
    role: Roles
    is_active: bool



class UserCreate(UserBase):
    password: str



class DietBase(BaseModel):
    name: str
    description: str
    calories: int

    

class DietCreate(DietBase):
    email: str
    

class Diet(DietBase):
    email: str
