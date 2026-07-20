import json
import logging
from json import JSONDecodeError

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.database import SessionLocal
from app.modules.websocket.manager import manager

from app.modules.chat.services import (
    build_messages,
    generate_response,
    get_chat_history,
    get_latest_or_create_session,
    save_message,
    serialize_history,
)

logger = logging.getLogger(__name__)


def parse_client_message(raw_message: str) -> str:
    try:
        payload = json.loads(raw_message)
    except JSONDecodeError:
        return raw_message.strip()

    if isinstance(payload, dict):
        content = payload.get("content") or payload.get("message") or ""
        return str(content).strip()

    return str(payload).strip()


async def websocket_service(websocket: WebSocket, user_id: int):

    db: Session = SessionLocal()
    await manager.connect(websocket)

    try:
        session = get_latest_or_create_session(
            db=db,
            user_id=user_id,
            title="WebSocket Chat"
        )

        history = get_chat_history(db, session.id)

        await manager.send_json(
            websocket,
            {
                "type": "history",
                "session_id": session.id,
                "messages": serialize_history(history)
            }
        )

        while True:

            raw_message = await websocket.receive_text()
            user_text = parse_client_message(raw_message)

            if not user_text:
                await manager.send_json(
                    websocket,
                    {
                        "type": "error",
                        "content": "Message cannot be empty."
                    }
                )
                continue

            save_message(
                db=db,
                session_id=session.id,
                role="user",
                content=user_text
            )

            # Load history
            history = get_chat_history(db, session.id)

            messages = build_messages(history)

            # AI Response
            assistant_reply = await run_in_threadpool(
                generate_response,
                messages
            )

            # Save assistant reply
            save_message(
                db=db,
                session_id=session.id,
                role="assistant",
                content=assistant_reply
            )

            # Send to frontend
            await manager.send_json(
                websocket,
                {
                    "type": "message",
                    "role": "assistant",
                    "session_id": session.id,
                    "content": assistant_reply
                }
            )

    except WebSocketDisconnect:

        await manager.disconnect()

    except Exception:

        logger.exception("WebSocket chat service failed")

        try:
            await manager.send_json(
                websocket,
                {
                    "type": "error",
                    "content": "Chat connection failed. Please reconnect."
                }
            )
            await websocket.close(code=1011)
        except RuntimeError:
            pass

    finally:

        db.close()
