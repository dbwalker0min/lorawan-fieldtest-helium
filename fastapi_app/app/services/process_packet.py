from app.services.parse_port1 import parse_packet, Decoded
from app.schema.schema import Packet
from app.db.models import RawPacket, GatewayReception, Decoded
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.build_response import build_response
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.services.send_downlink import send_downlink_async

from hexdump import hexdump


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
        dev_eui=int(packet.deviceInfo.devEui, 16) - 2**63,
        dev_name=packet.deviceInfo.deviceName,
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

    print(raw_packet.id)

    result = await session.execute(
        select(RawPacket)
        .options(
            selectinload(RawPacket.gateways),
            selectinload(RawPacket.decoded_results)
        )
        .where(RawPacket.id == raw_packet.id)
    )
    raw_packet = result.scalar_one()
    # from the raw packet, create the response (assuming the port was 1 and the HDOP was better than 2)
    if raw_packet.decoded_results and raw_packet.decoded_results.hdop < 2:
        response = build_response(raw_packet)

        # send the response to the device
        await send_downlink_async(
            dev_eui=packet.deviceInfo.devEui,
            payload=response,
            fport=2,
            confirmed=False
        )

