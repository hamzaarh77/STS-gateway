from dataclasses import dataclass

from .Parameter import Parameter


@dataclass
class Tool:
    name: str
    description: str
    parameters: list[Parameter]
    http_endpoint: str
    http_method: str

    def __str__(self):
        return f"{self.http_method} {self.http_endpoint}, {self.name}"
