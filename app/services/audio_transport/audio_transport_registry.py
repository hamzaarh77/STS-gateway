from app.enums import AudioTransportType


class AudioTransportRegistry():
    _providers = {}

    @classmethod
    def register(cls, provider_type: AudioTransportType, provider_cls):
        cls._providers[provider_type] = provider_cls

    @classmethod
    def get(cls, provider_type: AudioTransportType):
        provider_cls = cls._providers.get(provider_type)

        return provider_cls()
