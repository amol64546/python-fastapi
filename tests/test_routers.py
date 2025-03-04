import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
from app.models.user import User  # Import the User model

client = TestClient(app)

# Mock user data for the test
mock_user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123"
}

def test_create_user():
    response = client.post("/users", json=mock_user_data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()["users"]
    assert isinstance(users, list)
    assert len(users) > 0

def test_get_user_by_id():
    user_id = "12345"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    user = response.json()["user"]
    assert user["username"] == "john_doe"
    assert user["email"] == "john@example.com"

def test_get_user_by_id_not_found():
    user_id = "nonexistent_id"
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_internal_error():
    def mock_insert_one(*args, **kwargs):
        raise Exception("Internal server error")
    
    mongodb_client.insert_one = mock_insert_one
    
    response = client.post("/users", json=mock_user_data)
    assert response.status_code == 500
    assert response.json() == {"detail": "Error creating user: Internal server error"}
