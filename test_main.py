import pytest

from faker import Faker
from httpx import AsyncClient

from app import app

fake = Faker()

test_user = {
    "username": fake.user_name(),
    "password": fake.word(),
    "permission": "full_access"
}

admin = {
    "username": "admin",
    "password": "admin",
    "permission": "full_access"
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post('api/v1/auth/registration', json=admin)
        print("Client is ready")
        yield client


@pytest.fixture(scope="session")
async def login(client):
    response = await client.post("api/v1/auth/login", data=test_user)
    token = response.json().get("access_token")
    yield token


@pytest.mark.anyio
async def test_registrate_admin(client):
    response = await client.post('api/v1/auth/registration', json=test_user)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_login(client):
    response = await client.post("api/v1/auth/login", data=test_user)
    token = response.json().get("access_token")
    assert response.status_code == 200
    assert token != ''
    assert response.json().get("token_type") == 'bearer'


@pytest.mark.anyio
async def test_wrong_password(client):
    wrong_pass_admin = {
        "username": "admin",
        "password": "wrong_password",
        "permission": "full_access"
    }
    response = await client.post("api/v1/auth/login", data=wrong_pass_admin)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_get_items(client, login):
    headers = {"Authorization": f"Bearer {login}"}
    response = await client.get(url="api/v1/items", params={"page": 1, "size": 5}, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 5


@pytest.mark.anyio
async def test_get_items_unauthorized(client):
    headers = {"Authorization": f"Bearer undefined"}
    response = await client.get(url="api/v1/items", params={"page": 1, "size": 5}, headers=headers)
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_item(client, login):
    headers = {"Authorization": f"Bearer {login}"}
    response = await client.get("api/v1/items/2", headers=headers)
    assert response.status_code == 200
    assert response.json() != {}


@pytest.mark.anyio
async def test_create_item(client, login):
    headers = {"Authorization": f"Bearer {login}"}
    test_item = {"name": fake.word(),
                 "description": fake.sentence(),
                 "category": "Cybernetic",
                 "quantity": fake.random_int(min=1, max=20),
                 "price": fake.random_int(min=1, max=20000) / 100
                 }
    response = await client.post("api/v1/items", json=test_item, headers=headers)
    assert response.status_code == 201
    assert response.json() != {}


@pytest.mark.anyio
async def test_delete_item(client, login):
    headers = {"Authorization": f"Bearer {login}"}
    test_item = {"name": fake.word(),
                 "description": fake.sentence(),
                 "category": "Gadget",
                 "quantity": fake.random_int(min=1, max=20),
                 "price": fake.random_int(min=1, max=20000) / 100
                 }
    response_creation = await client.post("api/v1/items", json=test_item, headers=headers)

    response = await client.delete(f"api/v1/items/{response_creation.json().get('id')}", headers=headers)
    assert response.status_code == 204


@pytest.mark.anyio
async def test_update_item(client, login):
    headers = {"Authorization": f"Bearer {login}"}
    test_item = {"name": fake.word(),
                 "description": fake.sentence(),
                 "category": "Gadget",
                 "quantity": fake.random_int(min=1, max=20),
                 "price": fake.random_int(min=1, max=20000) / 100
                 }
    response_creation = await client.post("api/v1/items", json=test_item, headers=headers)
    new_name = fake.word()
    response = await client.put(
        f"api/v1/items/{response_creation.json().get('id')}",
        json={"name": new_name},
        headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == new_name
