from fastapi import APIRouter
from fastapi import WebSocket

from app.controllers import VoiceController

voice = APIRouter()


@voice.websocket("/voice/{partner_id}")
async def voice_session(websocket: WebSocket, partner_id: str):

    await VoiceController.handle_voice_session(
        websocket=websocket,
        partner_id=partner_id
    )
