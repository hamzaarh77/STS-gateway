from app.services.sts_provider.sts_provider import STSProvider
from app.enums import STSProviderType
from app.services.sts_provider.sts_provider_registry import STSProviderRegistry
from app.services.message_handler import UltravoxMessageHandler
from app.services.tool_caller_service import ToolCallerService
from app.dto import StsConfigDTO
from app.entities import Tool

import os
import urllib.parse
import aiohttp
import websockets


class UltravoxProvider(STSProvider):
    def __init__(self, sts_config: StsConfigDTO):
        super().__init__(sts_config)

        self.api_key = os.getenv("ULTRAVOX_API_KEY")
        self.temperature = sts_config.temperature
        self.voice = sts_config.voice
        self.ws = None

    def get_message_handler(self, tool_caller: ToolCallerService, on_playback_clear=None):
        return UltravoxMessageHandler(
            tool_caller=tool_caller,
            on_playback_clear=on_playback_clear
        )

    async def _create_call(self) -> str:
        async with aiohttp.ClientSession() as session:
            headers = {"X-API-Key": self.api_key}
            body = {
                "systemPrompt": self.sts_config.system_prompt,
                "temperature": self.temperature,
                "languageHint": "fr",
                "medium": {
                    "serverWebSocket": {
                        "inputSampleRate": 48000,
                        "outputSampleRate": 48000,
                        "clientBufferSizeMs": 30000,
                    }
                }
            }

            if self.voice:
                body["voice"] = self.voice
            if self.sts_config.selected_tools:
                body["selectedTools"] = self.tools_to_provider_format(
                    self.sts_config.selected_tools)

            async with session.post("https://api.ultravox.ai/api/calls", headers=headers, json=body) as response:
                if not response.ok:
                    error_body = await response.text()
                    raise RuntimeError(
                        f"Ultravox API error {response.status}: {error_body}")

                response.raise_for_status()
                data = await response.json()
                join_url = data["joinUrl"]
                url_parts = list(urllib.parse.urlparse(join_url))
                query = dict(urllib.parse.parse_qsl(url_parts[4]))
                query["apiVersion"] = "1"
                url_parts[4] = urllib.parse.urlencode(query)
                return urllib.parse.urlunparse(url_parts)

    async def connect(self):
        join_url = await self._create_call()
        self.ws = await websockets.connect(join_url)

    async def send(self, audio_chunk: bytes):
        if not self.ws:
            raise RuntimeError(
                "WebSocket not connected. Call connect() first.")
        await self.ws.send(audio_chunk)

    async def receive(self):
        if not self.ws:
            raise RuntimeError(
                "WebSocket not connected. Call connect() first.")
        return await self.ws.recv()

    async def close(self):
        if self.ws:
            await self.ws.close()
            self.ws = None

    def tools_to_provider_format(self, tools: list[Tool]) -> list[dict]:
        """
            parse list of tool entities (neutral forme) into ultravox specific needs
        """
        ultravox_tools = []

        for tool in tools:
            dynamic_parameters = []
            for param in tool.parameters:
                dynamic_parameters.append({
                    "name": param.name,
                    "location": 4,
                    "schema": {
                        "type": param.type,
                        "description": param.description
                    },
                    "required": param.required
                })
            ultravox_tools.append({
                "temporaryTool": {
                    "modelToolName": tool.name,
                    "description": tool.description,
                    "dynamicParameters": dynamic_parameters,
                    "client": {}
                }
            })
        return ultravox_tools


# provider disponible dans le registre dés l'import
STSProviderRegistry.register(STSProviderType.ULTRAVOX, UltravoxProvider)
