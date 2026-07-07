from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_signup_updates_activity_participants():
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
