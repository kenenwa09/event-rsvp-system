from pydantic import BaseModel
from typing import List


class Rsvp(BaseModel):
    event_id: int
    name: str
    email: str
    
    model_config = {"from_attributes": True}    


class RsvpCreate(BaseModel):
    name: str
    email: str


class RsvpResponse(BaseModel):
    rsvps: List[Rsvp]
