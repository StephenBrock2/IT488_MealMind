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
    assert "jwt_token" in client.cookies


    # Call the decorator-protected endpoint with the JWT cookie
    dec_response = client.post("/api/user/testdecorator")
    assert dec_response.status_code == 200
    payload = dec_response.json()
    assert payload["username"] == username

    # Logout
    response = client.get("/api/user/logout")
    assert response.status_code == 200
    assert "jwt_token" not in client.cookies


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


def test_create_recipe_as_bob():
    # Login as bob
    response = client.post("/api/user/login", json={
        "username": "bob",
        "password": "bobpass",
    })

    # Create a recipe with a unique name
    recipe_title = f"test_{int(time.time())}"
    response = client.post("/api/recipe", json={
        "title": recipe_title,
        "instructions": "Mix ingredients and cook for 10 minutes.",
        "cook_time": 10,
        "ingredients": [
            {"name": "salt", "quantity": 1.0, "unit": "tsp"}
        ],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == recipe_title
    assert "id" in data
    assert data["cook_time"] == 10
    assert any(i["name"] == "salt" for i in data["ingredients"])
    recipe_id = data["id"]

        # Update the recipe
    updated_title = f"{recipe_title}_updated"
    response = client.put(f"/api/recipe/{recipe_id}", json={
        "title": updated_title,
        "instructions": "Updated instructions.",
        "cook_time": 30,
        "ingredients": [
            {"name": "pepper", "quantity": 0.5, "unit": "tsp"},
            {"name": "olive oil", "quantity": 2.0, "unit": "tbsp"},
        ],
    })
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == recipe_id
    assert updated["title"] == updated_title
    assert updated["instructions"] == "Updated instructions."
    assert updated["cook_time"] == 30
    ingredient_names = [i["name"] for i in updated["ingredients"]]
    assert "pepper" in ingredient_names
    assert "olive oil" in ingredient_names
    assert "salt" not in ingredient_names
    


    # Logout and try to update without auth
    client.get("/api/user/logout")
    response = client.put(f"/api/recipe/{recipe_id}", json={
        "title": updated_title,
        "instructions": "Should fail.",
        "cook_time": 5,
        "ingredients": [],
    })
    assert response.status_code == 401


        # Login as alice and try to update bob's recipe (should be forbidden)
    client.post("/api/user/login", json={
        "username": "alice",
        "password": "alicepass",
    })
    response = client.put(f"/api/recipe/{recipe_id}", json={
        "title": updated_title,
        "instructions": "Alice's hijack attempt.",
        "cook_time": 5,
        "ingredients": [],
    })
    assert response.status_code == 403

    # Login back as bob and delete the recipe
    client.post("/api/user/login", json={
        "username": "bob",
        "password": "bobpass",
    })
    response = client.delete(f"/api/recipe/{recipe_id}")
    assert response.status_code == 200

    # Verify the recipe is gone
    response = client.get(f"/api/recipe/{recipe_id}")
    assert response.status_code == 404












