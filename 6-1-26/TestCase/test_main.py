from fastapi.testclient import TestClient
from Crud_op.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "FastAPI is running"


def test_create_user():
    response = client.post(
        "/users",
        json={"name": "Dhruv", "age": 22, "email": "dhruv@test.com"}
    )
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_users():
    client.post(
        "/users",
        json={"name": "A", "age": 20, "email": "a@test.com"}
    )

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_user():
    create = client.post(
        "/users",
        json={"name": "Test", "age": 25, "email": "test@test.com"}
    )
    user_id = create.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test"


def test_update_user():
    create = client.post(
        "/users",
        json={"name": "Old", "age": 30, "email": "old@test.com"}
    )
    user_id = create.json()["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={"name": "New"}
    )
    assert response.status_code == 200


def test_delete_user():
    create = client.post(
        "/users",
        json={"name": "Delete", "age": 40, "email": "delete@test.com"}
    )
    user_id = create.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
