from app.services.parse_port1 import parse_packet
import pytest
from app.db.models import Decoded


def test_decode_valid():
    """This is a really simple test case that just checks that the packet is parsed correctly."""
    result = parse_packet('mnrY1oZHBAgLCA==')

    assert result.latitude == pytest.approx(37.4843052)
    assert result.longitude == pytest.approx(-121.9151265)
    assert result.altitude == 32
    assert result.hdop == pytest.approx(1.1)
    assert result.nsatellites == 8

def test_decode_valid2():
    """This is a really simple test case that just checks that the packet is parsed correctly."""
    result = parse_packet('mnrZ1oY/BAQJCw==')

    # 37.4843052, -121.9149545
    assert result.latitude == pytest.approx(37.4843052)
    assert result.longitude == pytest.approx(-121.9149545)
    assert result.altitude == 28
    assert result.hdop == pytest.approx(0.9)
    assert result.nsatellites == 11

