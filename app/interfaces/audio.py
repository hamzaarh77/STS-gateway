from abc import ABC, abstractmethod


class AudioInputInterface(ABC):
    @abstractmethod
    async def start(self, send_callback):
        pass


class AudioOutputInterface(ABC):
    @abstractmethod
    def play(self, data: bytes):
        pass

    @abstractmethod
    def drop_buffer(self):
        pass
