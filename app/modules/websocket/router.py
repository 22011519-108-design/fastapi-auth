from fastapi import APIRouter, Query, WebSocket

from app.core.security import verify_access_token
from app.modules.websocket.service import websocket_service

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str | None = Query(default=None),
):
    if token is None:
        await websocket.close(code=1008)
        return

    payload = verify_access_token(token)

    if payload is None:
        await websocket.close(code=1008)
        return

    try:
        user_id = int(payload["user_id"])
    except (KeyError, TypeError, ValueError):
        await websocket.close(code=1008)
        return

    await websocket_service(
        websocket=websocket,
        user_id=user_id
    )
