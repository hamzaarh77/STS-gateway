from app.interfaces import AudioOutputInterface

import threading

import numpy as np
import sounddevice as sd


RATE = 48000
CHANNELS = 1


class SoundDeviceSpeaker(AudioOutputInterface):
    def __init__(self):
        self._buffer = bytearray()
        self._lock = threading.Lock()
        self._stream = sd.OutputStream(
            samplerate=RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=RATE // 100,
            callback=self._callback,
        )
        self._stream.start()

    def _callback(self, outdata: np.ndarray, frame_count, _time, _status):
        byte_count = frame_count * 2
        with self._lock:
            chunk = bytes(self._buffer[:byte_count])
            self._buffer[:] = self._buffer[byte_count:]
        if len(chunk) < byte_count:
            chunk += b"\x00" * (byte_count - len(chunk))
        outdata[:] = np.frombuffer(
            chunk, dtype="int16").reshape((frame_count, 1))

    def play(self, data: bytes):
        with self._lock:
            self._buffer.extend(data)

    def drop_buffer(self):
        with self._lock:
            self._buffer.clear()

    def close(self):
        if self._stream:
            self._stream.close()
