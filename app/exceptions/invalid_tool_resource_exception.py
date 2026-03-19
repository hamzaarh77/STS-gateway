from typing import List


class InvalidToolResourceException(Exception):
    def __init__(self, used_tool_name: str, valid_tools: List[str]):
        super().__init__(
            f"Invalid tool ressource {used_tool_name}. Valid tool ressources are: {', '.join(valid_tools)}")
