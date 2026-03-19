from dataclasses import dataclass
from typing import Optional

from app.entities import Tool


@dataclass
class StsConfigDTO:
    system_prompt: str
    greeting: str
    language: str
    voice: str
    temperature: float
    max_duration: int
    selected_tools: list[Tool]
    model: Optional[str]
    first_speaker: Optional[str]
