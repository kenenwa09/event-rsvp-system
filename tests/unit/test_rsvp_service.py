import pytest
from app.storage.storage import rsvp, events
from app.service.rsvp_service import RsvpService
from app.schemas.errors import NotFoundError


# first clear the storage before each test:
@pytest.fixture(autouse=True)
def clear_memories():
    rsvp.clear()
    events.clear()


# testing create rsvp when there is no event and-
# without event id
# it works because there is no event yet,-
# so NotFoundError is called.
def test_create_rsvp_no_event_id():
    with pytest.raises(NotFoundError):
        RsvpService.create_rsvp(event_id=1, name="chika", email="chika@mail.com")


# testing create rsvp with event id
def test_create_rsvp_success():
    # create fake event
    events[1] = {
        "id": 1,
        "title": "Tech Event",
        "description": "Desc",
        "date": "2026-01-01",
        "location": "Lagos",
        "flyer": None,
    }

    # initialize rsvp
    rsvp[1] = []

    # call Service
    response = RsvpService.create_rsvp(event_id=1, name="ola", email="ola@mail.com")

    assert response == [{"event_id": 1, "name": "ola", "email": "ola@mail.com"}]

    assert len(rsvp[1]) == 1


# testing get rsvp with no event id
def test_get_rsvp_no_event_id():
    with pytest.raises(NotFoundError):
        RsvpService.get_rsvp(event_id=1)


# testing get rsvp when event exist and rsvp-
# exists as well
def test_get_rsvp_success():
    events[1] = {
        "id": 1,
        "title": "Tech Event",
        "description": "Desc",
        "date": "2026-01-01",
        "location": "Lagos",
        "flyer": None,
    }

    rsvp[1] = [
        {"event_id": 1, "name": "Ade", "email": "ade@mail.com"},
        {"event_id": 1, "name": "Ugo", "email": "ugo@mail.com"},
    ]

    response = RsvpService.get_rsvp(event_id=1)

    assert response == {
        "rsvps": [
            {"event_id": 1, "name": "Ade", "email": "ade@mail.com"},
            {"event_id": 1, "name": "Ugo", "email": "ugo@mail.com"},
        ]
    }
