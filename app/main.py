from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.db.database import create_db_and_tables
from app.core.config import settings

app = FastAPI(title="LoRaWAN Field Test")

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

app.include_router(api_router)