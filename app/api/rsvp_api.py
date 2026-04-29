from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.rsvp import RsvpCreate, RsvpResponse, Rsvp
from app.service.rsvp_service import RsvpService
from app.schemas.errors import NotFoundError
from app.core.deps import get_async_db


router = APIRouter()


@router.post("/{event_id}", response_model=RsvpResponse, status_code=status.HTTP_201_CREATED)
async def create_rsvp_api(
    event_id: int,
    data: RsvpCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        rsvps = await RsvpService.create_rsvp(
            db=db, event_id=event_id, name=data.name, email=data.email
        )
        return {"rsvps": [Rsvp.model_validate(r) for r in rsvps]}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{event_id}", response_model=RsvpResponse, status_code=status.HTTP_200_OK)
async def get_rsvps(
    event_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        rsvps = await RsvpService.get_rsvp(db=db, event_id=event_id)
        return {"rsvps": [Rsvp.model_validate(r) for r in rsvps]}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))