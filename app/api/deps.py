from fastapi import Form, File, UploadFile
from typing import Optional, Tuple
from app.schemas.event import CreateEvent


async def event_datas(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    flyer: Optional[UploadFile] = File(None),
) -> Tuple[CreateEvent, Optional[str], Optional[bytes]]:

    new_event = CreateEvent(
        title=title,
        description=description,
        date=date,
        location=location,
    )

    flyer_filename = None
    flyer_bytes = None

    if flyer:
        flyer_filename = flyer.filename
        flyer_bytes = await flyer.read()

    return new_event, flyer_filename, flyer_bytes
