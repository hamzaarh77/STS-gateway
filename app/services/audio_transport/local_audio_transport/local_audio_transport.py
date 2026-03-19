from .sound_device_microphone import SoundDeviceMicrophone
from .sound_device_speaker import SoundDeviceSpeaker
from app.services.audio_transport import AudioTransport
from app.services.audio_transport.audio_transport_registry import AudioTransportRegistry
from app.enums import AudioTransportType


class LocalAudioTransport(AudioTransport):
    def __init__(self):
        self.micro = SoundDeviceMicrophone()
        self.speaker = SoundDeviceSpeaker()

    async def start(self, send_callback):
        await self.micro.start(send_callback)

    def play(self, data: bytes):
        self.speaker.play(data)

    def drop_buffer(self):
        self.speaker.drop_buffer()

    def close(self):
        self.speaker.close()


AudioTransportRegistry.register(AudioTransportType.LOCAL, LocalAudioTransport)
