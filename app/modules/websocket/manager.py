import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    async def disconnect(self):
        logger.info("Client disconnected")

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def send_json(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)


manager = ConnectionManager()
