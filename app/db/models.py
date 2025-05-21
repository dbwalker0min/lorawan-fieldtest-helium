from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List


class RawPacket(SQLModel, table=True):
    """Raw packet data from the LoRaWAN network server."""
    id: int = Field(default=None, primary_key=True)
    time: datetime
    fPort: int
    fCnt: int
    data: str

    gateways: List["GatewayReception"] = Relationship(
        back_populates="raw_packet", 
        sa_relationship_kwargs=dict(cascade="all, delete-orphan")
        )
    # a decoded result does not need to be present for a raw packet
    decoded_results: Optional["Decoded"] = Relationship(
        back_populates="raw_packet", 
        sa_relationship_kwargs=dict(cascade="all, delete-orphan")
        )


class GatewayReception(SQLModel, table=True):
    """Gateway reception data for a raw packet."""
    id: int = Field(default=None, primary_key=True)
    raw_packet_id: int = Field(foreign_key="rawpacket.id", nullable=False)
    rssi: float
    snr: float
    name: str
    lat: float
    long: float

    raw_packet: Optional[RawPacket] = Relationship(back_populates="gateways")


class Decoded(SQLModel, table=True):
    """Decoded result data for a raw packet."""
    id: int = Field(default=None, primary_key=True)
    raw_packet_id: int = Field(foreign_key="rawpacket.id")
    latitude: float
    longitude: float
    altitude: float
    hdop: float
    nsatellites: int

    raw_packet: Optional[RawPacket] = Relationship(back_populates="decoded_results")
