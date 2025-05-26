from fastapi import APIRouter, Depends
from app.schema.schema import Packet
from app.services.process_packet import process_packet
from app.db.database import get_session
from sqlmodel import Session
from pprint import pprint

router = APIRouter()

@router.post("/")
async def receive_packet(packet: Packet, session: Session = Depends(get_session)):
    print("Received packet:")
    pprint(packet.model_dump())
    await process_packet(packet, session)
    return {"message": "Packet received"}
