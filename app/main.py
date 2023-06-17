from typing import Union
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import model, schema, crud

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return f'Welcome to the Home Page!'


@app.post("/user")
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    get_user = crud.get_user_by_email(db, user.email)
    if get_user:
        print(get_user)
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)
    # print(user)
    

