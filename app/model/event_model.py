from typing import TYPE_CHECKING
from app.core.db_async import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.model.rsvp_model import Rsvp


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[str] = mapped_column(String(20))
    location: Mapped[str] = mapped_column(String(100))
    flyer: Mapped[str | None] = mapped_column(String(200), nullable=True) 

    rsvps: Mapped[list["Rsvp"]] = relationship("Rsvp", back_populates="event")