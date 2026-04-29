import os
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.model.event_model import Event
from app.schemas.errors import UnprocessableContentError, UnsupportedMediaError


class EventService:

    @staticmethod
    async def create_event(
        db: AsyncSession,
        title: str,
        description: str,
        date: str,
        location: str,
        flyer_filename: Optional[str] = None,
        flyer_bytes: Optional[bytes] = None,
    ) -> Event:

        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        saved_filename = None

        if flyer_filename and not flyer_bytes:
            raise UnprocessableContentError("File content is required")

        if flyer_bytes and not flyer_filename:
            raise UnprocessableContentError("File name is required")

        if flyer_bytes and flyer_filename:
            _, ext = os.path.splitext(flyer_filename)
            ext = ext.lower()

            allowed_extensions = {".png", ".jpg", ".jpeg", ".pdf"}

            if not ext:
                raise UnprocessableContentError("File must include extension")

            if ext not in allowed_extensions:
                raise UnsupportedMediaError("Unsupported file type")

            unique_name = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(upload_folder, unique_name)

            with open(file_path, "wb") as f:
                f.write(flyer_bytes)

            saved_filename = unique_name

        event = Event(
            title=title,
            description=description,
            date=date,
            location=location,
            flyer=saved_filename,
        )

        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    @staticmethod
    async def list_all_events(db: AsyncSession) -> list[Event]:
        result = await db.execute(select(Event))
        return list(result.scalars().all())