from fastapi import WebSocket, WebSocketDisconnect

from app.modules.websocket.manager import manager


async def websocket_service(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(
                websocket,
                f"You said: {data}"
            )

    except WebSocketDisconnect:
        await manager.disconnect()
        