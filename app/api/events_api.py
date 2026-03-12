from fastapi import File, UploadFile, HTTPException, status, Form, APIRouter, Depends
from app.schemas.event import CreateEvent
from app.api.deps import event_datas
from app.schemas.errors import UnprocessableContentError, UnsupportedMediaError
from app.schemas.event import EventResponse
from app.service.event_service import EventService


router = APIRouter()


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event_api(data=Depends(event_datas)):
    event_datas, flyer_filename, flyer_bytes = data
    try:
        event = EventService.create_event(
            title=event_datas.title,
            description=event_datas.description,
            date=event_datas.date,
            location=event_datas.location,
            flyer_filename=flyer_filename,
            flyer_bytes=flyer_bytes,
        )

        return event
    except UnprocessableContentError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except UnsupportedMediaError as e:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e)
        )


@router.get("/", response_model=list[EventResponse], status_code=status.HTTP_200_OK)
async def list_events():
    return EventService.list_all_events()
