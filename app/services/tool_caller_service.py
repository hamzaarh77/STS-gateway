import os
import requests

from app.entities import Tool
from app.exceptions import InvalidToolResourceException


class ToolCallerService:

    def __init__(self, tools: list[Tool]):
        self.base_url = os.getenv("TOOLS_PROVIDER_BASE_URL")
        self._registry = {tool.name: tool for tool in tools}

    def execute(self, name: str, arguments: dict) -> dict:
        tool = self._registry.get(name)
        if not tool:
            raise InvalidToolResourceException(
                name, list(self._registry.keys()))

        url = f"{self.base_url.rstrip('/')}/{tool.http_endpoint.lstrip('/')}"

        response = requests.request(
            method=tool.http_method,
            url=url,
            json=arguments,
        )

        response.raise_for_status()
        return response.json()
