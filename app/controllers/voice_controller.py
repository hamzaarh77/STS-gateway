import os

from fastapi import WebSocket

from app.services.sts_provider import STSProviderFacade
from app.services.audio_transport import AudioTransportFacade
from app.services.tool_caller_service import ToolCallerService
from app.services.voice_session_entry_point import VoiceSessionEntryPoint
from app.services.sts_provider.sts_config_service import StsConfigService


class VoiceController:
    @staticmethod
    async def handle_voice_session(websocket: WebSocket, partner_id):
        await websocket.accept()

        partner_context = StsConfigService.get_sts_config(
            partner_id)

        # strategy STS
        sts = STSProviderFacade.get_sts_provider(
            os.getenv("STS_PROVIDER"),
            partner_context
        )

        # audio transport strategy
        transport = AudioTransportFacade.get_audio_transport(
            os.getenv("AUDIO_TRANSPORT_STRATEGY")
        )

        # message handler
        message_handler = sts.get_message_handler(
            ToolCallerService(partner_context.selected_tools),
            transport.drop_buffer
        )

        try:
            await VoiceSessionEntryPoint.start(sts, transport, message_handler)
        finally:
            transport.close()
            await sts.close()
            await websocket.close()
