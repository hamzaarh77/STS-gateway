import json
from pathlib import Path

from .base_file_manager import BaseFileManager


class JsonFileManager(BaseFileManager):

    def read(self, file_path: Path) -> list | dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write(self, file_path: Path, content: dict):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
