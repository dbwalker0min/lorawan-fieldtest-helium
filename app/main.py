import sys
import asyncio

print("set event loop...", sys.platform)
if sys.platform.startswith("win"):
    print('Windows detected, setting WindowsSelectorEventLoopPolicy...')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
print("done with event loop setup.")

from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.db.database import create_db_and_tables
app = FastAPI(title="LoRaWAN Field Test")


@app.on_event("startup")
async def startup_event():
    print('Starting up the LoRaWAN Field Test application...')
    await create_db_and_tables()
    print('Database tables created successfully.')

app.include_router(api_router)
