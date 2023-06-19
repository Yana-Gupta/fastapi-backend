from fastapi.testclient import TestClient

def get_user_access_token( client: TestClient, email: str, password: str):

    r = client.post("/login", json={"email": email, "password": password})
    return r.json()["token"]

def create_user(client: TestClient, email: str, password: str, name: str, daily_calories: int, role: str):
    r = client.post("/user", json={"email": email, "password": password, "name": name,"daily_calories": daily_calories, "role": role})
    return r.json()


def create_user_and_return_access_token(client: TestClient, email: str, password: str, name: str, daily_calories: int, role: str):
    create_user(client=client, email=email, password=password, name=name, daily_calories=daily_calories, role=role)
    return get_user_access_token(client=client, email=email, password=password)