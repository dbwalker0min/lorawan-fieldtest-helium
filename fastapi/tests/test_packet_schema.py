import json
from pathlib import Path
from app.schema.schema import Packet
import os
from pprint import pprint
import pytest
from datetime import datetime

def test_packet_schema():
    # Load the test JSON file
    test_json_path = os.path.join(os.path.dirname(__file__), "test.json")
    with open(test_json_path, "r") as f:
        data_packets = json.load(f)

    for data in data_packets:
        # Parse with Pydantic schema
        packet = Packet(**data)

        # Assert required fields
        assert packet.time == datetime.fromisoformat(data["time"])
        assert packet.fCnt == data["fCnt"]
        assert packet.fPort == data["fPort"]
        assert packet.data == data["data"]

        # Check rxInfo fields
        rx = packet.rxInfo[0]
        rx_data = data["rxInfo"][0]
        assert rx.rssi == rx_data["rssi"]
        assert rx.snr == rx_data["snr"]
        assert rx.metadata.gateway_name == rx_data["metadata"]["gateway_name"]
        assert rx.metadata.gateway_lat == pytest.approx(float(rx_data["metadata"]["gateway_lat"]))
        assert rx.metadata.gateway_long == pytest.approx(float(rx_data["metadata"]["gateway_long"]))
