from fastapi import APIRouter, WebSocket

from app.modules.websocket.service import websocket_service

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_service(websocket)