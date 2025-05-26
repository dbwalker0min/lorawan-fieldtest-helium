from app.db.models import RawPacket, GatewayReception, Decoded
import math
from hexdump import hexdump


def compute_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """compute the distance between two points on the earth's surface."""
    dlat = 60*abs(lat2 - lat1)
    dlon = abs(lon2 - lon1)
    avg_lat = (lat1 + lat2) / 2

    if dlon > 180:
        dlon = abs(360 - dlon)

    dlon *= 60 * math.cos(avg_lat * math.pi / 180)

    M_PER_MINUTE = 1852
    return math.sqrt((dlat**2) + (dlon**2)) * M_PER_MINUTE


def build_response(raw_packet: RawPacket) -> bytes:

    # find the minium and maximum RSSI and minimum and maximum distance
    min_rssi = min_distance = math.inf
    max_rssi = max_distance = -math.inf
    ngateways = len(raw_packet.gateways)

    for gateway in raw_packet.gateways:
        min_rssi = min(min_rssi, gateway.rssi)
        max_rssi = max(max_rssi, gateway.rssi)
        distance = compute_distance(
            raw_packet.decoded_results.latitude,
            raw_packet.decoded_results.longitude,
            gateway.lat,
            gateway.long
        )
        min_distance = min(min_distance, distance)
        max_distance = max(max_distance, distance)
    
    # Force the RSSI values (plus 200) to be in the range of 0-255. This represents the range from -200 to 55 dBm.
    min_rssi = int(min(max(min_rssi + 200, 0), 255))
    max_rssi = int(min(max(max_rssi + 200, 0), 255))

    # scale the distance to a multiple of 250 meters. The minimum value is 250 meters.
    min_distance = int(min(max(round(min_distance/250), 1), 255))
    max_distance = int(min(max(round(max_distance/250), 1), 255))

    print(f"min_rssi: {min_rssi}, max_rssi: {max_rssi}, min_distance: {min_distance}, max_distance: {max_distance}, ngateways: {ngateways}")

    message = bytes([
        raw_packet.fCnt % 256,
        min_rssi,
        max_rssi,
        min_distance,
        max_distance,
        ngateways
    ])

    hexdump(message)
    return message
    