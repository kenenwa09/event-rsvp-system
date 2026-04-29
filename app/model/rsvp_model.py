from typing import TYPE_CHECKING
from app.core.db_async import Base
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.model.event_model import Event


class Rsvp(Base):
    __tablename__ = "rsvps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)  # removed unique=True

    event: Mapped["Event"] = relationship("Event", back_populates="rsvps")