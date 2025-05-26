import os
import pytest
from app.services.send_downlink import send_downlink_async, get_device_queue, flush_device_queue

@pytest.mark.asyncio
@pytest.mark.integration
async def test_send_downlink_integration():
    dev_eui = "0000000000000001"
    token = os.environ.get("HELIUM_API_TOKEN")

    assert token, "CHIRPSTACK_API_TOKEN not set"

    await flush_device_queue(dev_eui)
    queue_items = await get_device_queue(dev_eui)

    result = await send_downlink_async(dev_eui, b"\x05\x06\x08\x09", 10)

    queue_items = await get_device_queue(dev_eui)
    assert len(queue_items) == 1
