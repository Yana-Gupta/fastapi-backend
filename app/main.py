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
    return "<h1>Welcome to the home page of this api</h1>"



@app.get("/user/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    get_user = crud.get_user_by_email(db=db, email=email)
    if get_user is not None:
        return get_user
    else:
        return HTTPException(status_code=404, detail="User Not Found")



@app.post("/user")
def create_user( user: schema.UserCreate, db: Session = Depends(get_db)):
    get_user = crud.get_user_by_email(db, email=user.email)
    if get_user is not None:
        return HTTPException(status_code=400, detail="Email already registered")
    else:
        return crud.create_user(db=db, user=user)
    

@app.post("/diet")
def create_new_diet( diet: schema.DietCreate, db: Session = Depends(get_db)):
    return crud.create_diet(diet=diet, db=db)

