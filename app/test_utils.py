from fastapi.testclient import TestClient

TEST_ADMIN = "admin@gmail.com"
TEST_ADMIN_PASSWORD = "admin123"
TEST_ADMIN_NAME = "admin"
TEST_ADMIN_DAILY_CALORIES = 2332
TEST_ADMIN_ROLE = "admin"


TEST_USER_MANAGER = "manager@gmail.com"
TEST_USER_MANAGER_PASSWORD = "manager123"
TEST_USER_MANAGER_NAME = "manager"
TEST_USER_MANAGER_DAILY_CALORIES = 2332
TEST_USER_MANAGER_ROLE = "user_manager"

def get_user_access_token( client: TestClient, email: str, password: str):
    r = client.post("/login", json={"email": email, "password": password})
    return r.json()["token"]


def create_user(client: TestClient, email: str, password: str, name: str, daily_calories: int, role: str):
    r = client.post("/user", json={"email": email, "password": password, "name": name,"daily_calories": daily_calories, "role": role})
    return r.json()


def create_user_and_return_access_token(client: TestClient, email: str, password: str, name: str, daily_calories: int, role: str):
    create_user(client=client, email=email, password=password, name=name, daily_calories=daily_calories, role=role)
    return get_user_access_token(client=client, email=email, password=password)


def get_diet_for_user(client: TestClient, email: str, password: str):
    access_token = get_user_access_token(client=client, email=email, password=password)
    responses = client.post("/diet", headers={"Authorization": f"Bearer {access_token}"}, json={"name": "test_diet", "description": "test_description", "calories": 1234})
    r = client.get("/diet/{email}", headers={"Authorization": f"Bearer {access_token}"})
    responses = r.json()
    if responses is not None:
        print(responses)
        return responses
    

def get_token_for_admin(client: TestClient):
    r = client.post("/user", json={"email": TEST_ADMIN, "password": TEST_ADMIN_PASSWORD, "name": TEST_ADMIN_NAME,"daily_calories": TEST_ADMIN_DAILY_CALORIES, "role": TEST_ADMIN_ROLE})
    access_token = get_user_access_token(client=client, email=TEST_ADMIN, password=TEST_ADMIN_PASSWORD)
    return access_token


def get_token_for_user_manager(client: TestClient):
    r = client.post("/user",  json={"email": TEST_USER_MANAGER, "password": TEST_USER_MANAGER_PASSWORD, "name": TEST_USER_MANAGER_NAME,"daily_calories": TEST_USER_MANAGER_DAILY_CALORIES, "role": TEST_USER_MANAGER_ROLE})
    access_token = get_user_access_token(client=client, email=TEST_USER_MANAGER, password=TEST_USER_MANAGER_PASSWORD)
    return access_token
