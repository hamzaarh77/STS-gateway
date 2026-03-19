import json
import logging

from app.services.tool_caller_service import ToolCallerService
from app.exceptions import InvalidToolResourceException
from app.enums import UltravoxMessageType
from .base_message_handler import BaseMessageHandler

logger = logging.getLogger(__name__)


class UltravoxMessageHandler(BaseMessageHandler):
    def __init__(self, tool_caller: ToolCallerService, on_playback_clear=None):
        super().__init__(tool_caller, on_playback_clear)

    async def handle(self, message: str, send_callback):
        decoded = json.loads(message)
        msg_type = decoded.get("type")

        if msg_type == UltravoxMessageType.PLAYBACK_CLEAR_BUFFER.value:
            if self.on_playback_clear:
                self.on_playback_clear()

        elif msg_type == UltravoxMessageType.CLIENT_TOOL_INVOCATION.value:
            await self._handle_tool_call(decoded, send_callback)

        elif msg_type == UltravoxMessageType.STATE.value:
            logger.info(f"State: {decoded.get('state')}")

        elif msg_type == UltravoxMessageType.TRANSCRIPT.value:
            if decoded.get("role") == "agent" and decoded.get("final"):
                logger.info(
                    f"Agent: {decoded.get('text', decoded.get('delta', ''))}"
                )

    async def _handle_tool_call(self, msg: dict, send_callback):

        tool_name = msg["toolName"]
        invocation_id = msg["invocationId"]
        parameters = msg["parameters"]

        if isinstance(parameters, str):
            parameters = json.loads(parameters)

        logger.info(f"Tool call: {tool_name} with {parameters}")

        response = {
            "type": UltravoxMessageType.CLIENT_TOOL_RESULT.value,
            "invocationId": invocation_id,
        }

        try:
            result = self.tool_caller.execute(tool_name, parameters)
            if "error" in result:
                response["errorType"] = "execution_error"
                response["errorMessage"] = result["error"]
                await send_callback(json.dumps(response))
                return

            response["result"] = json.dumps(result)
        except InvalidToolResourceException as e:
            # TODO: relance au sts en lui précisent son erreur:
            logger.error(f"error in tool name, {str(e)}", exc_info=True)
            response["errorType"] = "tool_calling_error"
            response["errorMessage"] = str(e)

        except Exception as e:
            logger.error(
                f"Tool call '{tool_name}' raised an exception: {e}", exc_info=True)
            response["errorType"] = "execution_error"
            response["errorMessage"] = str(e)

        await send_callback(json.dumps(response))
