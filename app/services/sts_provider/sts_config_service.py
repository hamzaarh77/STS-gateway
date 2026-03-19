import os
import requests

from app.dto import StsConfigDTO
from app.utils.openapi.openapi_parser import OpenApiParser


class StsConfigService():

    @staticmethod
    def get_sts_config(partner_id: str) -> StsConfigDTO:

        base_url = os.getenv("TOOLS_PROVIDER_BASE_URL")

        response = requests.get(
            f"{base_url}/api/partner-context/{partner_id}", timeout=5)
        response.raise_for_status()
        json_data = response.json()

        data = json_data.get("data", {})
        sts_config = data.get("stsConfig", {})
        tools = data.get("tools", [])

        return StsConfigDTO(
            system_prompt=sts_config.get("system_prompt"),
            greeting=sts_config.get("greeting"),
            language=sts_config.get("language"),
            temperature=sts_config.get("temperature"),
            max_duration=sts_config.get("max_duration"),
            voice=sts_config.get("voice"),
            first_speaker=sts_config.get("first_speaker"),
            model=sts_config.get("model"),
            selected_tools=[
                tool for item in tools
                if (tool := OpenApiParser.get_tool(item))
            ]
        )
