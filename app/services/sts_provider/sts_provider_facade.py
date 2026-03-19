from app.services.sts_provider.sts_provider_registry import STSProviderRegistry
from app.enums import STSProviderType
from app.dto import StsConfigDTO


class STSProviderFacade:

    @staticmethod
    def get_sts_provider(provider_type: STSProviderType, sts_config: StsConfigDTO):
        return STSProviderRegistry.get(provider_type, sts_config)
