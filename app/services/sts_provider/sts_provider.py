from abc import ABC, abstractmethod

from app.services.tool_caller_service import ToolCallerService
from app.dto import StsConfigDTO
from app.entities import Tool


class STSProvider(ABC):
    def __init__(self, sts_config: StsConfigDTO):
        self.sts_config = sts_config

    @abstractmethod
    def get_message_handler(self, tool_caller: ToolCallerService, on_playback_clear=None):
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def send(self, audio_chunk: bytes):
        pass

    @abstractmethod
    async def receive(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    def tools_to_provider_format(self, tools: list[Tool]):
        pass
