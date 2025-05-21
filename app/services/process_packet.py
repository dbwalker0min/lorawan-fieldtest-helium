from app.services.parse_port1 import parse_packet, Decoded
from app.schema.schema import Packet
from app.db.models import RawPacket, GatewayReception, Decoded
from sqlmodel.ext.asyncio.session import AsyncSession


async def process_packet(packet: Packet, session: AsyncSession) -> None:
    """
    Processes a packet and writes the results to the database.
    """
    # Decode the packet data
    if packet.fPort == 1:
        # Decode the packet data
        decoded_data = parse_packet(packet.data)
    else:
        decoded_data = None

    gateways = [
        GatewayReception(
            name=rx.metadata.gateway_name,
            lat=rx.metadata.gateway_lat,
            long=rx.metadata.gateway_long,
            rssi=rx.rssi,
            snr=rx.snr
        ) for rx in packet.rxInfo
    ]

    # Create the RawPacket object
    raw_packet = RawPacket(
        time=packet.time,
        fPort=packet.fPort,
        fCnt=packet.fCnt,
        data=packet.data,
        gateways=gateways,
        decoded_results=decoded_data
    )

    session.add(raw_packet)
    await session.commit()
    await session.refresh(raw_packet)

