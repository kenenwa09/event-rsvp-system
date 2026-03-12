from fastapi import FastAPI, File, UploadFile, HTTPException, status, Form, APIRouter
from app.schemas.rsvp import RsvpCreate, RsvpResponse
from app.storage.storage import rsvp
from app.service.rsvp_service import RsvpService
from app.schemas.errors import NotFoundError


router = APIRouter()


@router.post(
    "/{event_id}", response_model=RsvpResponse, status_code=status.HTTP_201_CREATED
)
async def create_rsvp_api(event_id: int, data: RsvpCreate):
    try:
        rsvp = RsvpService.create_rsvp(
            event_id=event_id, name=data.name, email=data.email
        )

        return {"rsvps": rsvp}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{event_id}", response_model=RsvpResponse, status_code=status.HTTP_200_OK)
async def get_rsvps(event_id: int):
    try:
        return RsvpService.get_rsvp(event_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
