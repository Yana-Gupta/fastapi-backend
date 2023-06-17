from fastapi import Depends
from sqlalchemy.orm import Session
import model, schema


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def create_user(db: Session, user: model.User):
    # print(user)
    new_user = model.User(name=user.name, email=user.email, hashed_password=user.password, is_active=user.is_active, role=user.role)
    db.add(new_user)
    db.commit()
    # db.refresh(new_user)
    return f"user Created with id {user.name}"
    