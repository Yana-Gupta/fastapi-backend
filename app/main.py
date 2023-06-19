from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import SessionLocal, engine
from app import model
from app import schema
from app import crud
app = FastAPI()

model.Base.metadata.create_all(bind=engine)

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return "<h1>Welcome to the home page of this api</h1>"


@app.get('/user')
def get_users( db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.get_users(db=db, jwt_token=jwt_token.credentials)


@app.get("/user/{email}")
def get_user(email: str, db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    get_user = crud.get_user_by_email(db=db, email=email, jwt_token=jwt_token.credentials)
    if get_user is not None:
        return crud.get_user
    else:
        return HTTPException(status_code=404, detail="User Not Found")


@app.post("/user")
def create_user( user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.put("/user")
def update_user( user: schema.UserUpdate, db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.update_user(db=db, user=user, jwt_token=jwt_token.credentials)
    

@app.post("/login")
def auth (user: schema.UserBase, db: Session = Depends(get_db)):
    return crud.auth_user(db=db, user=user)

@app.get("/diet")
def get_diets( db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.get_all_diets(db=db, jwt_token=jwt_token.credentials)
    

@app.post("/diet")
def create_new_diet( diet: schema.DietCreate, db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.create_diet(diet=diet, db=db, jwt_token=jwt_token.credentials)


@app.get("/diet/{email}")
def get_diets_for_user(email: str, db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.get_diets_for_user(db=db, user=email, jwt_token=jwt_token.credentials)


@app.put("/diet/{id}")
def update_diet(id: int, diet: schema.DietUpdate, db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.update_diet(db=db, id=id, diet=diet, jwt_token=jwt_token.credentials)


@app.delete("/diet/{id}")
def delete_diet(id: int, db: Session = Depends(get_db), jwt_token: HTTPAuthorizationCredentials = Depends(security)):
    return crud.delete_diet(db=db, id=id, jwt_token=jwt_token.credentials)