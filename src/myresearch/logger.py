import logging
import asyncio


async def send_message(websocket, message):
    await websocket.send_json({"type": "log", "payload": message})


class WebSocketHandler(logging.Handler):
    def __init__(self, websocket, loop):
        super().__init__()
        self.websocket = websocket
        self.loop = loop

    def emit(self, record):
        try:
            msg = self.format(record)
            asyncio.run_coroutine_threadsafe(send_message(self.websocket, msg), self.loop)
        except Exception as e:
            # Handle exceptions (optional)
            raise e

