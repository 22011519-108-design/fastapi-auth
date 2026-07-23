import json
import logging
import traceback
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
from app.modules.agents.orchestrator import (
    run_orchestrator,
    classify_request,
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

            print("\n" + "=" * 60)
            print("USER MESSAGE:", user_text)

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

            history = get_chat_history(db, session.id)
            messages = build_messages(history)

            print("History loaded:", len(history))

            agent_type = classify_request(user_text)
            print("Agent selected:", agent_type)

            if agent_type == "catalog":

                print("Running Catalog Agent...")

                assistant_reply = await run_in_threadpool(
                    run_orchestrator,
                    agent_type="catalog",
                    payload={
                        "tool": "search_books",
                        "arguments": {
                            "query": user_text
                        }
                    },
                    db=db
                )

            else:

                print("Running Policy Agent...")

                assistant_reply = await run_in_threadpool(
                    run_orchestrator,
                    agent_type="policy",
                    payload={
                        "query": user_text
                    },
                    db=db
                )

            print("Assistant Reply:")
            print(assistant_reply)
            print("=" * 60)

            db_content = (
                json.dumps(assistant_reply)
                if isinstance(assistant_reply, dict)
                else assistant_reply
            )

            save_message(
                db=db,
                session_id=session.id,
                role="assistant",
                content=db_content
            )

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
        print("WebSocket disconnected.")
        await manager.disconnect()

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR INSIDE WEBSOCKET SERVICE")
        traceback.print_exc()
        print("=" * 60)

        logger.exception("WebSocket chat service failed")

        try:
            await manager.send_json(
                websocket,
                {
                    "type": "error",
                    "content": str(e)
                }
            )
            await websocket.close(code=1011)
        except RuntimeError:
            pass

    finally:
        db.close()