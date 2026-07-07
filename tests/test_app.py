from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]


def test_signup_adds_participant_to_activity():
    original_participants = activities["Chess Club"]["participants"][:]
    email = "new.student@mergington.edu"

    try:
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        updated_activity = client.get("/activities").json()["Chess Club"]
        assert email in updated_activity["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants


def test_signup_rejects_duplicate_participant():
    email = "michael@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant_from_activity():
    original_participants = activities["Chess Club"]["participants"][:]
    email = "test.remove@mergington.edu"

    activities["Chess Club"]["participants"].append(email)

    try:
        response = client.delete(f"/activities/Chess Club/participants/{email}")

        assert response.status_code == 200
        updated_activity = client.get("/activities").json()["Chess Club"]
        assert email not in updated_activity["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants
