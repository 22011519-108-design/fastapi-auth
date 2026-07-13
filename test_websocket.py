import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")

        await websocket.send("Hello Server")

        response = await websocket.recv()

        print("Server response:", response)


asyncio.run(test())
