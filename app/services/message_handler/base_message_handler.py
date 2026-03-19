from abc import ABC, abstractmethod

from app.services.tool_caller_service import ToolCallerService


class BaseMessageHandler(ABC):
    def __init__(self, tool_caller: ToolCallerService, on_playback_clear=None):
        self.tool_caller = tool_caller
        self.on_playback_clear = on_playback_clear

    @abstractmethod
    async def handle(self, message: str, send_callback):
        pass
