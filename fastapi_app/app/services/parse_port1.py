import binascii
from app.db.models import Decoded


def parse_packet(packet: str) -> Decoded:
    """
    Parses a packet and returns a dictionary with the parsed data.
    """
    # convert from base64 to bytes
    packet_bytes = binascii.a2b_base64(packet)

    b0 = packet_bytes[0]
    lng_sign = 1 if b0 & 0x80 == 0 else -1
    lat_sign = 1 if b0 & 0x40 == 0 else -1

    lat23 = (int.from_bytes(packet_bytes[0:4], byteorder='big', signed=False) >> 7) & 0x7F_FFFF
    lng23 = (int.from_bytes(packet_bytes[3:6], byteorder='big', signed=False) >> 0) & 0x7F_FFFF

    lat = lat_sign * min(lat23 * 108.0 / 10e6, 90)
    lng = lng_sign * min(lng23 * 215   / 10e6, 180)

    alt = int.from_bytes(packet_bytes[6:8], byteorder='big', signed=False) - 1000

    hdop = packet_bytes[8]/10
    nsatellites = packet_bytes[9]

    return Decoded(
        latitude=lat,
        longitude=lng,
        altitude=alt,
        hdop=hdop,
        nsatellites=nsatellites
    )