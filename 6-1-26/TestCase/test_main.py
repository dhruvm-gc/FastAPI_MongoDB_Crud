from fastapi.testclient import TestClient
from bson import ObjectId
from Crud_op.main import app
from Crud_op import routes

# -----------------------------
# Fake MongoDB collection
# -----------------------------

class FakeInsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class FakeUpdateResult:
    def __init__(self, matched_count):
        self.matched_count = matched_count


class FakeDeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


class FakeCollection:
    def __init__(self):
        self.data = {}

    def insert_one(self, doc):
        _id = ObjectId()
        doc["_id"] = _id
        self.data[_id] = doc
        return FakeInsertResult(_id)

    def find(self):
        return self.data.values()

    def find_one(self, query):
        return self.data.get(query["_id"])

    def update_one(self, query, update):
        _id = query["_id"]
        if _id not in self.data:
            return FakeUpdateResult(0)

        self.data[_id].update(update["$set"])
        return FakeUpdateResult(1)

    def delete_one(self, query):
        _id = query["_id"]
        if _id in self.data:
            del self.data[_id]
            return FakeDeleteResult(1)

        return FakeDeleteResult(0)


# -----------------------------
# Override real MongoDB
# -----------------------------

routes.collection = FakeCollection()
client = TestClient(app)

# -----------------------------
# Tests
# -----------------------------

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
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


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
    assert response.json()["message"] == "User updated"


def test_delete_user():
    create = client.post(
        "/users",
        json={"name": "Delete", "age": 40, "email": "delete@test.com"}
    )
    user_id = create.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"
