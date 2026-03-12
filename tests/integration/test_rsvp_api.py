import pytest
from fastapi.testclient import TestClient
from app.storage.storage import rsvp, events
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_memory():
    rsvp.clear()
    events.clear()


def test_create_rsvp_without_event():
    response = client.post("/rsvp/1", json={"name": "Ify", "email": "ify@mail.com"})

    assert response.status_code == 404


def test_create_rsvp_success():
    event_response = client.post(
        "/event",
        data={
            "title": "Reunion",
            "description": "Meeting old school mates",
            "date": "02-03-2026",
            "location": "Enugu",
        },
    )

    assert event_response.status_code == 201

    response = client.post("/rsvp/1", json={"name": "Ify", "email": "ify@mail.com"})

    assert response.status_code == 201

    data = response.json()

    assert data == {"rsvps": [{"event_id": 1, "name": "Ify", "email": "ify@mail.com"}]}


def test_create_multiple_rsvp():
    event_response = client.post(
        "/event",
        data={
            "title": "Reunion 3",
            "description": "Meeting old school mates 3",
            "date": "02-06-2026",
            "location": "Enugu 3",
        },
    )

    assert event_response.status_code == 201

    client.post("/rsvp/1", json={"name": "chi", "email": "chi@mail.com"})

    response = client.post("/rsvp/1", json={"name": "Didi", "email": "didi@mail.com"})

    assert response.status_code == 201

    data = response.json()

    assert data == {
        "rsvps": [
            {"event_id": 1, "name": "chi", "email": "chi@mail.com"},
            {"event_id": 1, "name": "Didi", "email": "didi@mail.com"},
        ]
    }


def test_create_rsvp_missing_email():
    event_response = client.post(
        "/event",
        data={
            "title": "Reunion 3",
            "description": "Meeting old school mates 3",
            "date": "02-06-2026",
            "location": "Enugu 3",
        },
    )

    assert event_response.status_code == 201

    response = client.post("/rsvp/1", json={"name": "mark"})

    assert response.status_code == 422


def test_get_rsvps_no_event():
    response = client.get("/rsvp/1")

    assert response.status_code == 404


def test_get_rsvps_success():
    event_response = client.post(
        "/event",
        data={
            "title": "Reunion 3",
            "description": "Meeting old school mates 3",
            "date": "02-06-2026",
            "location": "Enugu 3",
        },
    )

    assert event_response.status_code == 201

    client.post("/rsvp/1", json={"name": "jude", "email": "jude@mail.com"})

    rsvp_response = client.post(
        "/rsvp/1", json={"name": "edu", "email": "edu@mail.com"}
    )

    assert rsvp_response.status_code == 201

    response = client.get("/rsvp/1")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "rsvps": [
            {"event_id": 1, "name": "jude", "email": "jude@mail.com"},
            {"event_id": 1, "name": "edu", "email": "edu@mail.com"},
        ]
    }
