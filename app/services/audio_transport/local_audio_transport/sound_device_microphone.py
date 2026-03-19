from app.interfaces import AudioInputInterface

import asyncio

import sounddevice as sd

RATE = 48000
CHANNELS = 1


class SoundDeviceMicrophone(AudioInputInterface):
    async def start(self, send_callback):
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[bytes] = asyncio.Queue()

        def callback(indata, _frame_count, _time, _status):
            loop.call_soon_threadsafe(queue.put_nowait, indata.tobytes())

        stream = sd.InputStream(
            samplerate=RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=RATE // 100,
            callback=callback,
        )
        with stream:
            while True:
                data = await queue.get()
                await send_callback(data)
