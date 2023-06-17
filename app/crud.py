from fastapi import Depends
from sqlalchemy.orm import Session
import model, schema


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def create_user(db: Session, user: schema.UserCreate):
    new_user = model.User(name=user.name, email=user.email, role=user.role, hashed_password=user.password, is_active=user.is_active)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_diet(db: Session, diet: schema.DietCreate):
    new_diet = model.Diet(email=diet.email, name=diet.name, description=diet.description, calories=diet.calories)
    db.add(new_diet)
    db.commit()
    db.refresh(new_diet)
    print(new_diet)
    return new_diet


def get_diet_for_user(db: Session, email: str):
    return db.query(model.Diet).filter(model.Diet.email == email)
