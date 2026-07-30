from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import app as app_module


def test_unregister_participant_removes_them_from_activity():
    client = TestClient(app_module.app)
    original_participants = app_module.activities["Chess Club"]["participants"][:]

    try:
        response = client.delete(
            "/activities/Chess%20Club/participants/michael@mergington.edu"
        )

        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

        updated_activities = client.get("/activities").json()
        assert "michael@mergington.edu" not in updated_activities["Chess Club"]["participants"]
    finally:
        app_module.activities["Chess Club"]["participants"] = original_participants
