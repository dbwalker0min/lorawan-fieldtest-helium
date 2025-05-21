import json
from fastapi.testclient import TestClient
from app.api.endpoints import app


def test_receive_packet():
    # Load your test JSON
    print("Loading test JSON")
    with open("test/test.json", "r") as f:
        data = json.load(f)

    client = TestClient(app)
    for packet in data:

        response = client.post("/", json=packet)
        assert response.status_code == 200
        assert response.json() == {"message": "Packet received"}
