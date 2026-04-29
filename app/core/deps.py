from app.core.db_sync import SyncSessionLocal
from app.core.db_async import AsyncSessionLocal

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()   
        
        
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db        