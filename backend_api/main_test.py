import pytest
import random
import time
from fastapi.testclient import TestClient
from main import app
from dependencies import state_change

# Switch to dev (in-memory) mode for testing
state_change(app, "prod")

client = TestClient(app)


def test_count_increments():
    r1 = client.get("/api/count")
    assert r1.status_code == 200
    val1 = r1.json()

    r2 = client.get("/api/count")
    assert r2.status_code == 200
    val2 = r2.json()

    assert val2 == val1 + 1


def test_ingredient_post_then_get():
    created_ids = []
    rand = random.randint(1000, 9999)

    apple_name = f"test{rand}_apple"
    apple_juice_name = f"test{rand}_apple juice"
    tomato_juice_name = f"test{rand}_tomato juice"

    response = client.post("/api/ingredient", json={"name": apple_name, "quantity": 2, "unit": "whole"})
    assert response.status_code == 200
    json = response.json()
    assert json["name"] == apple_name
    created_ids.append(json["id"])

    response = client.post("/api/ingredient", json={"name": apple_juice_name, "quantity": 1, "unit": "cup"})
    assert response.status_code == 200
    json = response.json()
    assert json["name"] == apple_juice_name
    created_ids.append(json["id"])

    response = client.post("/api/ingredient", json={"name": tomato_juice_name, "quantity": 1, "unit": "cup"})
    assert response.status_code == 200
    json = response.json()
    assert json["name"] == tomato_juice_name
    created_ids.append(json["id"])

    response = client.get("/api/ingredient", params={"name": f"test{rand}_tomato"})
    assert response.status_code == 200
    json = response.json()
    ingredient_names = [i["name"] for i in json["ingredients"]]
    assert tomato_juice_name in ingredient_names

    response = client.get("/api/ingredient", params={"name": f"test{rand}_apple"})
    assert response.status_code == 200
    json = response.json()
    ingredient_names = [i["name"] for i in json["ingredients"]]
    assert apple_name in ingredient_names
    assert apple_juice_name in ingredient_names

    for ingredient_id in created_ids:
        client.delete(f"/api/ingredient/{ingredient_id}")

    response = client.get("/api/ingredient", params={"name": f"test{rand}"})
    assert response.status_code == 200
    json = response.json()
    assert json["ingredients"] == []


def test_ingredient_post_missing_name():
    response = client.post("/api/ingredient", json={})
    assert response.status_code == 422


def test_user_test_password_verification():
    response = client.post("/api/user/test")
    assert response.status_code == 200
    result = response.json()
    assert result == [True, True]



def test_user_login():
    username = f"test_login{int(time.time())}"
    password = f"{username}pass"

    # Register first
    response = client.post("/api/user/register", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": password,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert "id" in data


    # Login with correct credentials
    response = client.post("/api/user/login", json={
        "username": username,
        "password": password,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert "id" in data


    # Call the decorator-protected endpoint with the JWT cookie
    dec_response = client.post("/api/user/testdecorator")
    assert dec_response.status_code == 200
    payload = dec_response.json()
    assert payload["username"] == username

    # Logout
    response = client.get("/api/user/logout")
    assert response.status_code == 200


    # Call without a JWT cookie
    # client.cookies.clear()
    dec_response = client.post("/api/user/testdecorator")
    assert dec_response.status_code == 401

    # Login with wrong password
    response = client.post("/api/user/login", json={
        "username": username,
        "password": "wrongpassword",
    })
    assert response.status_code == 404



