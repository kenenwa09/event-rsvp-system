from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.events_api import router as event_router
from app.api.rsvp_api import router as rsvp_router
from app.core.db_async import engine, Base

import app.model.event_model  
import app.model.rsvp_model   


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    


app = FastAPI(lifespan=lifespan)

app.include_router(event_router, prefix="/event", tags=["Event"])
app.include_router(rsvp_router, prefix="/rsvp", tags=["Rsvp"])