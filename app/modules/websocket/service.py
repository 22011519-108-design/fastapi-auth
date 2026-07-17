from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.modules.websocket.manager import manager

from app.modules.chat.models import ChatSession, ChatMessage
from app.modules.chat.services import build_messages, generate_response


async def websocket_service(websocket: WebSocket):

    db: Session = SessionLocal()

    await manager.connect(websocket)

    # Demo: user_id from JWT baad mein dynamic kar lena
    user_id = 1

    session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
        .first()
    )

    if session is None:

        session = ChatSession(
            user_id=user_id,
            title="WebSocket Chat"
        )

        db.add(session)
        db.commit()
        db.refresh(session)

    try:

        while True:

            user_text = await websocket.receive_text()

            # Save user message
            db.add(
                ChatMessage(
                    session_id=session.id,
                    role="user",
                    content=user_text
                )
            )

            db.commit()

            # Load history
            history = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session.id)
                .order_by(ChatMessage.created_at)
                .all()
            )

            messages = build_messages(history)

            # AI Response
            assistant_reply = generate_response(messages)

            # Save assistant reply
            db.add(
                ChatMessage(
                    session_id=session.id,
                    role="assistant",
                    content=assistant_reply
                )
            )

            db.commit()

            # Send to frontend
            await manager.send_message(
                websocket,
                assistant_reply
            )

    except WebSocketDisconnect:

        await manager.disconnect()

    finally:

        db.close()