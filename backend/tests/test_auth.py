from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_signup():
    response = client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "username": "testuser", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert "token" in data

def test_login():
    # First signup
    client.post(
        "/api/auth/signup",
        json={"email": "login@example.com", "username": "loginuser", "password": "password123"}
    )
    
    # Then login
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "login@example.com"
    assert "token" in data

def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
