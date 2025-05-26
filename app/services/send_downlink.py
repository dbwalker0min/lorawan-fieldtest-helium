import httpx
import base64
import asyncio
import os

def validate_deveui(deveui: str):
    """
    Validates the DevEUI format."""
    assert len(deveui) == 16, "DevEUI must be exactly 16 characters"
    try:
        int(deveui, 16)
    except ValueError:
        assert False, "DevEUI must be a valid hex string"


async def send_downlink_async(dev_eui: str, payload: bytes, fport: int, confirmed: bool = False) -> str:
    """
    Asynchronously sends a downlink message to a LoRaWAN device via ChirpStack REST API.
    
    Args:
        dev_eui (str): The 16-char DevEUI of the device.
        payload (bytes): Raw bytes to send.
        fport (int): LoRaWAN FPort (1–255).
        confirmed (bool): Whether the message requires confirmation.
    
    Returns:
        str: Queue item ID of the sent downlink message.
    """
    print(f"Sending downlink to {dev_eui} with payload {payload.hex()} on FPort {fport}, confirmed={confirmed}")
    validate_deveui(dev_eui)
    assert 1 <= fport <= 255, "FPort must be between 1 and 255"

    api_token = os.environ.get("HELIUM_API_TOKEN")
    if not api_token:
        raise RuntimeError("Missing HELIUM_API_TOKEN environment variable.")

    base_url = "https://console.iot-wireless.com"
    endpoint = f"/api/devices/{dev_eui}/queue"
    url = base_url + endpoint

    # Prepare the request
    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}"
    }

    data = {
        "queueItem": {
            "confirmed": confirmed,
            "fPort": fport,
            "data": base64.b64encode(payload).decode()
        }
    }

    # Send request
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        print(f"Response status: {response.status_code}, body: {response.text}")
        response.raise_for_status()  # Raise error if status not 2xx
        return response.json()['id']

async def get_device_queue(dev_eui: str) -> list[dict]:
    """
    Fetch the current queue items for a given device.
    """
    import httpx, os

    api_token = os.environ.get("HELIUM_API_TOKEN")
    if not api_token:
        raise RuntimeError("Missing HELIUM_API_TOKEN")

    url = f"https://console.iot-wireless.com/api/devices/{dev_eui}/queue"

    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return [r for r in response.json().get('result', [])]

async def flush_device_queue(dev_eui: str) -> None:
    """
    Clear all downlink queue items for a given device.
    """
    import httpx, os

    api_token = os.environ.get("HELIUM_API_TOKEN")
    if not api_token:
        raise RuntimeError("Missing HELIUM_API_TOKEN")

    url = f"https://console.iot-wireless.com/api/devices/{dev_eui}/queue"

    headers = {
        "accept": "application/json",
        "Grpc-Metadata-Authorization": f"Bearer {api_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        response.raise_for_status()
