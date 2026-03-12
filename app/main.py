from fastapi import FastAPI
from app.api.events_api import router as event_router
from app.api.rsvp_api import router as rsvp_router


app = FastAPI()

app.include_router(event_router, prefix=("/event"), tags=["Event"])
app.include_router(rsvp_router, prefix=("/rsvp"), tags=["Rsvp"])
