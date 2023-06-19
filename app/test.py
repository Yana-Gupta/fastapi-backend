from fastapi.testclient import TestClient

from app.main import app

from app import test_utils


client = TestClient(app)

TEST_EMAIL = "new@gmail.com"
TEST_PASSWORD = "test123"
TEST_NAME = "test"
TEST_DAILY_CALORIES = 2332
TEST_USER_ROLE = "user"


TEST_EMAIL1 = "new1@gmail.com"
TEST_PASSWORD1 = "test123"
TEST_NAME1 = "test1"
TEST_DAILY_CALORIES1 = 2332
TEST_USER_ROLE1 = "user"


TEST_ADMIN = "admin@gmail.com"
TEST_ADMIN_PASSWORD = "admin123"
TEST_ADMIN_NAME = "admin"
TEST_ADMIN_DAILY_CALORIES = 2332
TEST_ADMIN_ROLE = "admin"

def test_on_main():
    print("--------------------------------------------------------------")
    print("Testing the endpoint / ")
    responses = client.get("/")
    assert responses.status_code == 200 
    assert responses.json() == "<h1>Welcome to the home page of this api</h1>"


def test_create_user():
    print("----------------------------------------------------------")
    print("Testing the endpoint /user -> the endpoint is used to create a user ")
    responses = client.post("/user", json={"email": TEST_EMAIL, "password": TEST_PASSWORD, "name": TEST_NAME,"daily_calories": TEST_DAILY_CALORIES, "role": TEST_USER_ROLE})
    assert responses.status_code == 201
    assert responses.json() == {"message": "User created successfully"}
    

def test_auth_user():
    responses = client.post("/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})   
    assert responses.status_code == 200
    assert responses.json()["token"] is not None


def test_only_auth_can_make_diet():
    responses = client.post("/diet", json={"name": "test_diet", "description": "test_description", "calories": 1234})
    assert responses.status_code == 403


def test_create_diet():
    access_token = test_utils.get_user_access_token(client=client, email=TEST_EMAIL, password=TEST_PASSWORD)
    assert access_token is not None
    responses = client.post("/diet", headers={"Authorization": f"Bearer {access_token}"}, json={"name": "test_diet", "description": "test_description", "calories": 1234})
    assert responses.status_code == 201
    assert responses.json() == {"message": "Diet created successfully"}


def test_only_user_can_get_diet():
    responses = client.get("/diet/{TEST_EMAIL}")
    assert responses.status_code == 403    


def test_only_user_can_get_diet1():
    token = test_utils.create_user_and_return_access_token(client=client, email=TEST_EMAIL1, password=TEST_PASSWORD1, name=TEST_NAME1, daily_calories=TEST_DAILY_CALORIES1, role=TEST_USER_ROLE1)

    responses = client.get("/diet/{TEST_EMAIL}", headers={"Authorization": f"Bearer {token}"})
    assert responses.json()["status_code"] == 401
    assert responses.json()["detail"] == "You are not authorized to view this user's diets"


def test_update_diet_fails_with_token():
    responses = client.put("/diet/1", json={"name": "test_diet", "description": "test_description", "calories": 1234})
    assert responses.status_code == 403


def test_get_all_user_fails_with_user_token():
    print("----------------------------------------------------------")
    print("Testing the endpoint /user -> the endpoint is used to get all users ... the route is only accessible to admin and user manager")
    access_token = test_utils.get_user_access_token(client=client, email=TEST_EMAIL, password=TEST_PASSWORD)
    assert access_token is not None
    responses = client.get("/user", headers={"Authorization": f"Bearer {access_token}"})
    assert responses.json()["error"] == "You are not admin or user manager!"



def test_get_all_user():
    print("----------------------------------------------------------")
    print("Testing the endpoint /user -> the endpoint is used to get all users ... the route is only accessible to admin and user manager")
    access_token = test_utils.get_token_for_admin(client=client)
    assert access_token is not None
    responses = client.get("/user", headers={"Authorization": f"Bearer {access_token}"})
    assert responses.status_code == 200
    assert responses.json() is not None



def test_get_all_diets_fails_not_accessible_for_user_manager():
    print("----------------------------------------------------------")
    print("Testing the endpoint /diet -> the endpoint is used to get all diets ... the route is only accessible to admin")
    access_token = test_utils.get_user_access_token(client=client, email=TEST_EMAIL, password=TEST_PASSWORD)
    assert access_token is not None
    responses = client.get("/diet", headers={"Authorization": f"Bearer {access_token}"})
    assert responses.json()["error"] == "You are not authorized to view all diets"

    access_token_for_user_manager = test_utils.get_token_for_user_manager(client=client)
    assert access_token_for_user_manager is not None
    responses = client.get("/diet", headers={"Authorization": f"Bearer {access_token_for_user_manager}"})
    assert responses.json()["error"] == "You are not authorized to view all diets"


