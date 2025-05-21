from fastapi import FastAPI, Depends
from app.schema.schema import Packet
from app.services.process_packet import process_packet
from app.db.database import get_session
from sqlmodel import Session

app = FastAPI()


@app.post("/")
async def receive_packet(packet: Packet, session: Session = Depends(get_session)):
    await process_packet(packet, session)
    return {"message": "Packet received"}
