from pydantic import BaseModel
from typing import Optional


class CreateEvent(BaseModel):
    title: str
    description: str
    date: str
    location: str


class EventResponse(CreateEvent):
    id: int
    flyer: Optional[str]



model_config = {"from_attributes": True}