import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 200
    assert f"Signed up {test_email} for {activity}" in response.json().get("message", "")
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response_dup.status_code == 400
    # Unregister
    response_del = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response_del.status_code == 200
    assert f"Removed {test_email} from {activity}" in response_del.json().get("message", "")
    # Unregister again (should fail)
    response_del2 = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response_del2.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/NonexistentActivity/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
