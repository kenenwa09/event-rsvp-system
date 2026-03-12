import os
import uuid
from app.storage.storage import events
from typing import Optional
from app.schemas.errors import UnprocessableContentError, UnsupportedMediaError


class EventService:
    @staticmethod
    def create_event(
        title: str,
        description: str,
        date: str,
        location: str,
        flyer_filename: Optional[str] = None,
        flyer_bytes: Optional[bytes] = None,
    ):

        event_id = len(events) + 1
        saved_filename = None

        # create a folder to safe the flyer if uploaded
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        if flyer_filename and not flyer_bytes:
            raise UnprocessableContentError("File content is required")

        if flyer_bytes and not flyer_filename:
            raise UnprocessableContentError("File name is required")

        if flyer_bytes and flyer_filename:
            # Extract and validate extension
            _, ext = os.path.splitext(flyer_filename)
            ext = ext.lower()

            allowed_extension = {".png", ".jpg", ".jpeg", ".pdf"}

            if not ext:
                raise UnprocessableContentError("File must include extension")

            if ext not in allowed_extension:
                raise UnsupportedMediaError("Unsupported file type")

            unique_name = f"{uuid.uuid4()}{ext}"

            # this file_path constructs the full file path where your uploaded flyer will be saved
            file_path = os.path.join(upload_folder, unique_name)

            with open(file_path, "wb") as f:
                f.write(flyer_bytes)

            saved_filename = unique_name

        event = {
            "id": event_id,
            "title": title,
            "description": description,
            "date": date,
            "location": location,
            "flyer": saved_filename,
        }

        events[event_id] = event
        return event

    @staticmethod
    def list_all_events():
        return list(events.values())
