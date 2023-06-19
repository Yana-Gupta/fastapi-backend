from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import func
from app.auth import jwt_handler
from app.schema import Roles
from app import model, schema, helper
from fastapi.responses import JSONResponse


def get_users(db: Session, jwt_token: str):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    if cred["decoded_token"]["role"] == Roles.admin or cred["decoded_token"]["role"] == Roles.user_manager:
        return db.query(model.User).all()
    return {"error": "You are not admin or user manager!"}


def get_user_by_email(db: Session, email: str, jwt_token: str):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    if cred["decoded_token"]["email"] == email or cred["decoded_token"]["role"] == Roles.admin or cred["decoded_token"]["role"] == Roles.user_manager:
        return db.query(model.User).filter(model.User.email == email).first()
    return { "error": "Invalid token"}


def create_user(db: Session, user: schema.UserCreate):
    get_user = db.query(model.User).filter(model.User.email == user.email).first()
    if get_user is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = model.User(name=user.name, email=user.email, role=user.role, hashed_password=user.password, daily_calories=user.daily_calories)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"})

def auth_user(db: Session, user: schema.UserCreate):
    get_user = db.query(model.User).filter(model.User.email == user.email).first()
    if get_user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if get_user.hashed_password != user.password:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user_role = get_user.role
    return jwt_handler.sign_JWT(user.email, user_role)


def update_user(db: Session, user: schema.UserUpdate, jwt_token):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    
    if cred["decoded_token"]["email"] == user.email or cred["decoded_token"]["role"] != Roles.admin or cred["decoded_token"]["role"] != Roles.user_manager:
        db.query(model.User).filter(model.User.email == user.email).update({"name": user.name, "hashed_password": user.password, "daily_calories": user.daily_calories})
        db.commit()
        return db.query(model.User).filter(model.User.email == user.email).first()
    return { "error": "unauthorized"}


def create_diet(db: Session, diet: schema.DietCreate, jwt_token):
    cred = jwt_handler.decodeJWT(jwt_token)

    if cred is False:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

    user_email = cred["decoded_token"]["email"]
    current_date = date.today()
    food_calories = diet.calories


    if food_calories == 0:
        food = diet.description
        calories = helper.get_food_nutrition(food)
        if calories is None:
            calories = 0
        else:    
            food_calories = calories.get("calories")
   
    get_diet = []
    can_take = True

    if food_calories == 0:
        can_take = True
    else: 
        get_diet = db.query(model.Diet).filter(model.Diet.email == user_email, func.date(model.Diet.date) == current_date).all()

    calories_taken = helper.get_all_calorie_count(get_diet)

    get_user = db.query(model.User).filter(model.User.email == user_email).first()
    if get_user.daily_calories < calories_taken + food_calories:
        can_take = False

    new_diet = model.Diet(email=user_email, name=diet.name, description=diet.description, calories=food_calories, isLessThan=can_take)
    db.add(new_diet)
    db.commit()
    db.refresh(new_diet)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Diet created successfully"})  



def get_diets_for_user(db: Session, user: str, jwt_token: str):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    if cred["decoded_token"]["email"] == user or cred["decoded_token"]["role"] == Roles.admin:
        diets = db.query(model.Diet).filter(model.Diet.email == user).all()
        return { "diets": diets}
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view this user's diets")



def update_diet(id: id,db: Session, diet: schema.DietUpdate, jwt_token):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    
    user_email = cred["decoded_token"]["email"]

    calories = diet.calories
    if calories == 0:
        calories=helper.get_food_nutrition(diet.description).get("calories")

    that_diet = db.get(model.Diet, id)
    all_diets = db.query(model.Diet).filter(model.Diet.email == user_email).all()
    print(that_diet.email)
    print(user_email)

    if that_diet is None:
        return { "error": "Invalid diet id"}
    
    if that_diet.email != user_email and cred["decoded_token"]["role"] != Roles.admin:
        return { "error": "You are not authorized to update this diet"}
    

    if calories is None: 
        calories = 0
   
    calories_taken = helper.get_all_calorie_count(all_diets) - that_diet.calories
    total_calories = get_calorie_amount_for_user(user_email, db)

    if ( calories_taken + calories ) > total_calories:
        that_diet.isLessThan = False
        that_diet.name = diet.name
        that_diet.description = diet.description
        that_diet.calories = calories
        db.commit()
    else: 
        that_diet.isLessThan = True
        that_diet.name = diet.name
        that_diet.description = diet.description
        that_diet.calories = calories
        db.commit()    

    return db.get(model.Diet, id)


def delete_diet(id: id, db: Session, jwt_token):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    
    user_email = cred["decoded_token"]["email"]

    that_diet = db.get(model.Diet, id)

    if that_diet is None:
        return { "error": "Invalid diet id"}

    if cred["decoded_token"]["role"] != Roles.admin and that_diet.email != user_email:
        return { "error": "You are not authorized to delete this diet"}
  
    db.delete(that_diet)
    db.commit()
    return { 
        "message": "Diet deleted successfully"
    }


def get_calorie_amount_for_user(email: str, db: Session):
    return db.query(model.User).filter(model.User.email == email).first().daily_calories


def get_all_diets(db: Session, jwt_token):
    cred = jwt_handler.decodeJWT(jwt_token)
    if cred is False:
        return {"error": "Invalid token"}
    
    if cred["decoded_token"]["role"] != Roles.admin:
        return { "error": "You are not authorized to view all diets"}
    diets = db.query(model.Diet).all()
    return { "diets": diets}