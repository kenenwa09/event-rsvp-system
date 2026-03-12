import os
import shutil
import pytest

from app.service.event_service import EventService
from app.schemas.errors import UnprocessableContentError, UnsupportedMediaError
from app.storage.storage import events

# run this before each test, to clear events and uploads:


# first clear the memory:
@pytest.fixture(autouse=True)
def clear_events_and_uploads():
    events.clear()

    # Remove uploads folder if it exists:
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")

    yield

    # Cleanup after test:
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")


def test_create_event_without_flyer():
    event = EventService.create_event(
        title="Tech Conference",
        description="Annual tech event",
        date="2026-05-10",
        location="Lagos",
    )

    assert event == {
        "id": 1,
        "title": "Tech Conference",
        "description": "Annual tech event",
        "date": "2026-05-10",
        "location": "Lagos",
        "flyer": None,
    }


def test_bytes_without_filename():
    with pytest.raises(UnprocessableContentError):
        EventService.create_event(
            title="Bazzar",
            description="Church event",
            date="2026-01-01",
            location="Anambra",
            flyer_bytes=b"flyerbytescontent",
        )


def test_filename_without_bytes():
    with pytest.raises(UnprocessableContentError):
        EventService.create_event(
            title="Bazzar",
            description="Church event",
            date="2026-01-01",
            location="Anambra",
            flyer_filename="pic.png",
        )


def test_unspported_extension():
    with pytest.raises(UnsupportedMediaError):
        EventService.create_event(
            title="Bazzar",
            description="Church event",
            date="2026-01-01",
            location="Anambra",
            flyer_filename="pic.exe",
            flyer_bytes=b"flyerbytescontent",
        )


def test_valid_file_upload():
    event = EventService.create_event(
        title="Music fest",
        description="Party",
        date="2026-07-01",
        location="Enugu",
        flyer_filename="music_pic.png",
        flyer_bytes=b"musiccontent",
    )

    assert event == {
        "id": 1,
        "title": "Music fest",
        "description": "Party",
        "date": "2026-07-01",
        "location": "Enugu",
        "flyer": event["flyer"],
    }

    assert event["flyer"] is not None
    assert event["flyer"].endswith(".png")


def test_list_all_events_empty():
    response = EventService.list_all_events()

    assert response == []
    assert isinstance(response, list)


def test_list_all_events_with_data():
    EventService.create_event(
        title="Event 1", description="Desc 1", date="2026-01-01", location="Lagos"
    )

    EventService.create_event(
        title="Event 2", description="Desc 2", date="2026-02-01", location="Abuja"
    )

    response = EventService.list_all_events()

    assert response == [
        {
            "id": 1,
            "title": "Event 1",
            "description": "Desc 1",
            "date": "2026-01-01",
            "location": "Lagos",
            "flyer": None,
        },
        {
            "id": 2,
            "title": "Event 2",
            "description": "Desc 2",
            "date": "2026-02-01",
            "location": "Abuja",
            "flyer": None,
        },
    ]
