from fastapi import WebSocket


class ConnectionManager:

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    async def disconnect(self):
        print("Client disconnected")

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)


manager = ConnectionManager()