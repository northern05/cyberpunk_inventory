from datetime import datetime

from fastapi.testclient import TestClient
from app import app

client = TestClient(app=app)


def test_get_items():
    response = client.get(url="api/v1/items", params={"page": 1, "size": 5})
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_get_item():
    response = client.get("api/v1/items/2")
    assert response.status_code == 200
    assert response.json() != {}


def test_create_item():
    test_item = {"name": "Gorilla Arms",
                 "description": "This implant allows you to deal more Physical damage in melee combat, and have a 10-20% chance to apply a Bleed effect.",
                 "category": "Cybernetic",
                 "quantity": 3,
                 "price": 3000.50
                 }
    response = client.post("api/v1/items", json=test_item)
    assert response.status_code == 201
    assert response.json() != {}


def test_delete_item():
    test_item = {"name": "test_delete_item",
                 "description": "test_delete_item",
                 "category": "Weapon",
                 "quantity": 3,
                 "price": 3
                 }
    response_creation = client.post("api/v1/items", json=test_item)

    response = client.delete(f"api/v1/items/{response_creation.json()['id']}")
    assert response.status_code == 204


def test_update_item():
    rand_element = datetime.now()
    response = client.put("api/v1/items/17", json={"name": f"test_update_{rand_element}"})
    assert response.status_code == 200
    assert response.json()["name"] == f"test_update_{rand_element}"

