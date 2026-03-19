from abc import ABC, abstractmethod


class AudioTransport(ABC):

    @abstractmethod
    async def start(self, send_callback):
        pass

    @abstractmethod
    def play(self, data: bytes):
        pass

    @abstractmethod
    def drop_buffer(self):
        pass

    @abstractmethod
    def close(self):
        pass
