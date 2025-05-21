from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


class Packet(BaseModel):

    class RxInfo(BaseModel):
        class GatewayMetadata(BaseModel):
            gateway_name: str
            gateway_lat: float
            gateway_long: float

        rssi: float
        snr: float
        metadata: GatewayMetadata

    time: datetime
    fCnt: int
    fPort: int
    data: str
    rxInfo: List[RxInfo]

    model_config = ConfigDict(from_attributes=True)
