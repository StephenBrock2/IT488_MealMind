import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_count_increments():
    r1 = client.get("/count")
    assert r1.status_code == 200
    val1 = r1.json()

    r2 = client.get("/count")
    assert r2.status_code == 200
    val2 = r2.json()

    assert val2 == val1 + 1


def test_ingredient_get():
    response = client.get("/ingredient", params={"name": "tomato"})
    assert response.status_code == 200
    json = response.json()
    assert {"name": "tomato"} in json["ingredients"]
    assert {"name": "tomato juice"} in json["ingredients"]

    response = client.get("/ingredient", params={"name": "apple"})
    assert response.status_code == 200
    json = response.json()
    assert {"name": "apple"} in json["ingredients"]
    assert {"name": "apple juice"} in json["ingredients"]


def test_ingredient_post():
    response = client.post("/ingredient", json={"name": "garlic"})
    assert response.status_code == 200
    json = response.json()
    assert json["name"] == "garlic"

    response = client.post("/ingredient", json={"name": "apple"})
    assert response.status_code == 200
    json = response.json()
    assert json["name"] == "apple"



def test_ingredient_post_missing_name():
    response = client.post("/ingredient", json={})
    assert response.status_code == 422
