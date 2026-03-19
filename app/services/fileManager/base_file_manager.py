from abc import ABC, abstractmethod
from pathlib import Path


class BaseFileManager(ABC):

    @abstractmethod
    def read(self, file_path: Path) -> list | dict:
        pass

    @abstractmethod
    def write(self, file_path: Path, content: dict):
        pass
