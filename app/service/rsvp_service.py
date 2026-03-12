from app.storage.storage import events, rsvp
from app.schemas.errors import NotFoundError


class RsvpService:

    @staticmethod
    def create_rsvp(event_id: int, name: str, email: str):
        if event_id not in events:
            raise NotFoundError("Event not found")
        new_rsvp = {"event_id": event_id, "name": name, "email": email}

        rsvp[event_id].append(new_rsvp)
        return rsvp[event_id]

    @staticmethod
    def get_rsvp(event_id: int):
        if event_id not in events:
            raise NotFoundError("Event not found")
        return {"rsvps": rsvp[event_id]}
