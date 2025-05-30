from pprint import pprint
import pytest_asyncio
import pytest
from sqlmodel import SQLModel, select
from app.db.models import RawPacket, GatewayReception, Decoded
from app.schema.schema import Packet as InputPacket
from app.services.process_packet import process_packet
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import os
import json
from unittest.mock import patch, AsyncMock


@pytest_asyncio.fixture(name="session", scope="function")
async def session_fixture():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", echo=False, future=True)
    async with AsyncSession(engine) as session:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        yield session


@pytest.mark.asyncio(loop_scope="function")
@patch("app.services.process_packet.send_downlink_async", new_callable=AsyncMock)
async def test_create_packet(mock_send_downlink, session: AsyncSession):

    # set the mock return value
    mock_send_downlink.return_value = "123"

    print("Starting test_create_packet")
    print(session, type(session))

    # Load the test JSON file
    test_json_path = os.path.join(os.path.dirname(__file__), "test.json")
    with open(test_json_path, "r") as f:
        data_packets = json.load(f)

    for data in data_packets:

        # form the input packet
        packet: InputPacket = InputPacket(**data)

        # process it
        await process_packet(packet, session)

    assert mock_send_downlink.await_count == 2  # Adjust this based on your test.json

    # Check number of RawPacket records
    raw_packet_count = await session.exec(select(RawPacket))
    gateway_count = await session.exec(select(GatewayReception))
    decoded_count = await session.exec(select(Decoded))

    assert len(raw_packet_count.all()) == 3
    assert len(gateway_count.all()) == 3
    assert len(decoded_count.all()) == 2
