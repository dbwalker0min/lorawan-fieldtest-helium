from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import AsyncGenerator
import os
from urllib.parse import quote
import socket
from pydantic import BaseSettings

class Settings(BaseSettings):
    POSTGRESQL_USER: str = "postgres"
    POSTGRESQL_PASSWD: str = "password"
    POSTGRESQL_HOST: str = "localhost"

    class Config:
        env_file = ".env"

settings = Settings()

# Quote the user and password to handle special characters
user = quote(settings.POSTGRESQL_USER)
passwd = quote(settings.POSTGRESQL_PASSWD)
DATABASE_URL = f"postgresql+psycopg://{user}:{passwd}@{settings.POSTGRESQL_HOST}:5432/tracker?sslmode=require"

print(f"Connecting to database at {DATABASE_URL}")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
