from enum import Enum


class UltravoxMessageType(Enum):
    CLIENT_TOOL_INVOCATION = "client_tool_invocation"
    CLIENT_TOOL_RESULT = "client_tool_result"
    STATE = "state"
    TRANSCRIPT = "transcript"
    PLAYBACK_CLEAR_BUFFER = "playback_clear_buffer"
    DEBUG = "debug"
