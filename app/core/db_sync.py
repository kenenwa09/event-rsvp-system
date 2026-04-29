from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

DATABASE_URL_SYNC = settings.DATABASE_URL_SYNC

engine = create_engine(
    DATABASE_URL_SYNC,
    echo=True if settings.ENVIRONMENT == "DEBUG" else False,
)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass