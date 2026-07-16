from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.models import ChatSession, ChatMessage
from app.modules.chat.services import build_messages, generate_response

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    # Create a new session if no session_id is provided
    if request.session_id is None:

        session = ChatSession(
            user_id=1,
            title="New Chat"
        )

        db.add(session)
        db.commit()
        db.refresh(session)

    # Otherwise fetch the existing session
    else:

        session = (
            db.query(ChatSession)
            .filter(ChatSession.id == request.session_id)
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Chat session not found."
            )

    # Save user message
    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        content=request.message
    )

    db.add(user_message)
    db.commit()

    # Load complete chat history
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at)
        .all()
    )

    # Convert history into LLM format
    messages = build_messages(history)

    # Generate assistant response
    assistant_response = generate_response(messages)

    # Save assistant response
    assistant_message = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=assistant_response
    )

    db.add(assistant_message)
    db.commit()

    return ChatResponse(
        session_id=session.id,
        response=assistant_response
    )