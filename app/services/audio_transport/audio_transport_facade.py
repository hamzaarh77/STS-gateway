from app.enums import AudioTransportType
from app.services.audio_transport.audio_transport_registry import AudioTransportRegistry


class AudioTransportFacade:
    @staticmethod
    def get_audio_transport(transport_type: AudioTransportType):
        return AudioTransportRegistry.get(transport_type)
