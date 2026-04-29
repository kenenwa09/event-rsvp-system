from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.model.event_model import Event
from app.model.rsvp_model import Rsvp
from app.schemas.errors import NotFoundError


class RsvpService:

    @staticmethod
    async def create_rsvp(
        db: AsyncSession, event_id: int, name: str, email: str
    ) -> list[Rsvp]:
        result = await db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()

        if not event:
            raise NotFoundError("Event not found")

        new_rsvp = Rsvp(event_id=event_id, name=name, email=email)
        db.add(new_rsvp)
        await db.commit()

        rsvp_result = await db.execute(select(Rsvp).where(Rsvp.event_id == event_id))
        return list(rsvp_result.scalars().all())

    @staticmethod
    async def get_rsvp(db: AsyncSession, event_id: int) -> list[Rsvp]:
        result = await db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()

        if not event:
            raise NotFoundError("Event not found")

        rsvp_result = await db.execute(select(Rsvp).where(Rsvp.event_id == event_id))
        return list(rsvp_result.scalars().all())