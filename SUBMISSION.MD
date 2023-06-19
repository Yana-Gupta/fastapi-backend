# Techstack Used 

[FASTAPI](https://fastapi.tiangolo.com/)


## How to run the project 

Install all teh dependencies module 

```
pip install -r requirements.txt
```

The main file is inside app directory, to start the fastapi run following command

```
uvicorn app.main:app --reload
```
**NOTE**: Make sure port 8000 of your localhost is not busy.

Visit the following route to access the data
```
http://localhost:8000/docs
```


### Project Testing 
Run the following command to run the test scripts 
```
pytest app/test.py
```
**NOTE**: To print the logs use follwing command
```
pytest --capture=no  app/test.py
```
**NOTE**: Change the TEST_EMAIL in `test.py` in `app` directory after running the test once.


## Endpoints Created 

- GET '/' Accessible to all 
- POST '/user' to create a user 
- GET '/user/{email}' only accessible to that user, admin or user manager
- POST '/login' return jwt 
- POST '/diet'creates a new diet 
- GET '/user' returns the list of all the user, only accessible to admin or user manager
- PUT '/user' updates the user information, only accessible to admin or user, or user manager
- GET '/diet/{email}' returns the list of all the diets of a user, only accessible to user or admin
- GET '/diet' return the list of all the diets, only accessible to the admin
- GET 'diet/{id}' only accessible to the user if the diet is his otherwise user can not access the information, admin can access the route
- DELETE 'diet/{id}' only accessible to the user if that diet is his otherwise can not access, admin can access the route



## Information about project

- User has 3 roles -> 1) User, 2) User Manager, 3) ADMIN

1) User - The user can create, read, update and delete the diet created by him
2) User Manager - The user manager can view all the routes associated with the user , e.g. GET all the users, access a particular user by email
3) Admin - Admin has access to all the routes including which user and user manager don't have access.


### Third api from where information is accessed.
[FoodData Central](https://fdc.nal.usda.gov/)

NOTE: Assumption: at initial the food_calories will be 0, if user inputs the food_calories himself, then data will not be fetched from the api otherwise data is fetched, and if user has entered any such meal for which data doesn't exits, then the food_calories will be set to 0.
