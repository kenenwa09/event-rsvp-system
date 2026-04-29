from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import event_datas
from app.core.deps import get_async_db
from app.schemas.errors import UnprocessableContentError, UnsupportedMediaError
from app.schemas.event import EventResponse
from app.service.event_service import EventService


router = APIRouter()


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event_api(
    data=Depends(event_datas),
    db: AsyncSession = Depends(get_async_db),
):
    event_data, flyer_filename, flyer_bytes = data
    try:
        event = await EventService.create_event(
            db=db,
            title=event_data.title,
            description=event_data.description,
            date=event_data.date,
            location=event_data.location,
            flyer_filename=flyer_filename,
            flyer_bytes=flyer_bytes,
        )
        return event
    except UnprocessableContentError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except UnsupportedMediaError as e:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e))


@router.get("/", response_model=list[EventResponse], status_code=status.HTTP_200_OK)
async def list_events(db: AsyncSession = Depends(get_async_db)):
    return await EventService.list_all_events(db)