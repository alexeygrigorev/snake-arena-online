from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    # Helper to get token
    response = client.post(
        "/api/auth/signup",
        json={"email": "leaderboard@example.com", "username": "leaderboarduser", "password": "password123"}
    )
    if response.status_code == 409:
        response = client.post(
            "/api/auth/login",
            json={"email": "leaderboard@example.com", "password": "password123"}
        )
    return response.json()["token"]

def test_submit_score():
    token = get_auth_token()
    response = client.post(
        "/api/leaderboard",
        json={"score": 100, "mode": "walls"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

def test_get_leaderboard():
    response = client.get("/api/leaderboard")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
