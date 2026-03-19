from app.enums import STSProviderType
from app.dto import StsConfigDTO


class STSProviderRegistry():
    _providers = {}

    @classmethod
    def register(cls, provider_type: STSProviderType, provider_cls):
        cls._providers[provider_type] = provider_cls

    @classmethod
    def get(cls, provider_type: STSProviderType, sts_config: StsConfigDTO):
        provider_cls = cls._providers.get(provider_type)

        return provider_cls(sts_config)
