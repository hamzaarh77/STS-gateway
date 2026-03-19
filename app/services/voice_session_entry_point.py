import asyncio

from app.services.sts_provider import STSProvider
from app.services.audio_transport import AudioTransport
from app.services.message_handler import BaseMessageHandler


class VoiceSessionEntryPoint():

    @staticmethod
    async def start(sts: STSProvider, audio_transport: AudioTransport, message_handler: BaseMessageHandler):
        await sts.connect()

        async def receiver():
            while True:
                message = await sts.receive()

                if isinstance(message, bytes):
                    audio_transport.play(message)
                    continue

                await message_handler.handle(message, sts.send)

        await asyncio.gather(
            audio_transport.start(sts.send),
            receiver()
        )
