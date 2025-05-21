import os
import json
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel
from httpx import AsyncClient
from app.api.endpoints import app
from app.db.database import get_session

@pytest_asyncio.fixture(scope="function")
async def session_fixture():
    if os.path.exists("test.db"):
        os.remove("test.db")
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)
    async with AsyncSession(engine) as session:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        yield session
        print("\n\nCleaning up the database...\n")
        await engine.dispose()

@pytest.mark.asyncio
async def test_receive_packet(session_fixture):
    # Dependency override
    async def override_get_session():
        yield session_fixture

    app.dependency_overrides[get_session] = override_get_session

    # Use httpx.AsyncClient with ASGITransport for async FastAPI testing
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open("test/test.json", "r") as f:
            data = json.load(f)
            
        for packet in data:
            response = await ac.post("/", json=packet)
            assert response.status_code == 200
            assert response.json() == {"message": "Packet received"}

    # Clean up override
    app.dependency_overrides.clear()
