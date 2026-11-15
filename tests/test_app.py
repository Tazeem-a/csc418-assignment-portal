import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
import app as portal

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(portal, "DATA_FILE", tmp_path / "submissions.json")
    portal.app.config.update(TESTING=True)
    with portal.app.test_client() as client:
        yield client

def test_complete_submission_is_saved_and_displayed(client):
    response = client.post("/", data={
        "name": "Tazeem", "reg_no": "SP23-BCS-039",
        "title": "DevOps Lab", "submission_url": "https://example.com/work"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Submission saved successfully" in response.data
    assert b"Tazeem" in response.data
    assert b"SP23-BCS-039" in response.data

def test_missing_registration_number_is_rejected(client):
    response = client.post("/", data={
        "name": "Tazeem", "reg_no": "",
        "title": "DevOps Lab", "submission_url": "https://example.com/work"
    })
    assert response.status_code == 200
    assert b"All fields are required" in response.data
    assert portal.load_submissions() == []

def test_invalid_submission_url_is_rejected_and_not_saved(client):
    response = client.post("/", data={
        "name": "Tazeem", "reg_no": "SP23-BCS-039",
        "title": "DevOps Lab", "submission_url": "not-a-url"
    })
    assert response.status_code == 200
    assert b"Please enter a valid" in response.data
    assert portal.load_submissions() == []
