from app.services.build_response import compute_distance
import pytest


def test_simple_compute_distance():
    """This is a really simple test case that just checks that the distance is computed correctly."""
    lat1 = 37.4843052
    lon1 = -121.9151265
    lat2 = 37.4843052
    lon2 = -121.9149545

    result = compute_distance(lat1, lon1, lat2, lon2)

    assert result == pytest.approx(15.16626335609231, rel=0.01)

def test_compute_distance_at_45N():
    """Test the distance calculation at the North Pole."""
    lat1 = 45.0
    lon1 = 0.0
    lat2 = 45.0
    lon2 = 0.01

    result = compute_distance(lat1, lon1, lat2, lon2)

    assert result == pytest.approx(786.0, abs=0.5)

def test_compute_distance_across_international_date_line():
    """Test the distance calculation across the International Date Line."""
    lat1 = 37.4843052
    lon1 = 180 - 0.01
    lat2 = 37.4843052
    lon2 = -180 + 0.01

    result = compute_distance(lat1, lon1, lat2, lon2)

    assert result == pytest.approx(1.764e3, abs=0.5)  # Should be very small due to rounding

def test_compute_distance_across_international_date_line_the_other_way():
    """Test the distance calculation across the International Date Line."""
    lat1 = 37.4843052
    lon2 = 180 - 0.01
    lat2 = 37.4843052
    lon1 = -180 + 0.01

    result = compute_distance(lat1, lon1, lat2, lon2)

    assert result == pytest.approx(1.764e3, abs=0.5)  # Should be very small due to rounding

def test_compute_distance_across_equator():
    """Test the distance calculation across the equator."""
    lat1 = 0.01
    lon1 = 34.0
    lat2 = -0.01
    lon2 = 34

    result = compute_distance(lat1, lon1, lat2, lon2)

    assert result == pytest.approx(2222, abs=0.5)  # Should be very small due to rounding

def test_compute_distance_near_the_north_pole():
    """Test the distance calculation near the North Pole."""
    lat1 = 89.0
    lon1 = 0.0
    lat2 = 89.0
    lon2 = 1

    result = compute_distance(lat1, lon1, lat2, lon2)

    assert result == pytest.approx(1939, rel=0.01)  # Should be very small due to rounding    