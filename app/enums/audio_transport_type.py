from enum import Enum


class AudioTransportType(str, Enum):
    LOCAL = "local"
    TWILIO = "twilio"
