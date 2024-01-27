import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from myresearch.logger import WebSocketHandler
from myresearch.main import custom_function
import asyncio

from myresearch.paths import static

app = FastAPI()
app.mount("/static", StaticFiles(directory=static), name="static")


@app.get("/")
def read_root():
    return HTMLResponse(content=open(static / "index.html", "r").read())


def run_function(logger, result_container):
    result_container["result"] = custom_function(custom_logger=logger)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("WebSocket Connection Established")

    try:
        result_container = {}
        while True:
            data = await websocket.receive_text()

            if data == "Run Command":
                loop = asyncio.get_running_loop()
                logger = logging.getLogger("custom_logger")
                logger.setLevel(logging.INFO)
                ws_handler = WebSocketHandler(websocket, loop)
                logger.addHandler(ws_handler)

                custom_function_thread = threading.Thread(target=run_function, args=(logger, result_container))
                custom_function_thread.start()

                while custom_function_thread.is_alive():
                    await asyncio.sleep(0.1)

                custom_function_thread.join()

                # Send the final result
                final_result = result_container.get("result", "No result")
                await websocket.send_text(final_result)
    finally:
        await websocket.send_text("Function completed.")
        await websocket.close()
