from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user_id
from app.core.dependencies import get_db
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.services import (
    build_messages,
    generate_response,
    get_chat_history,
    get_or_create_session,
    save_message,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):

    user_text = request.message.strip()

    if not user_text:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        session = get_or_create_session(
            db=db,
            user_id=current_user_id,
            session_id=request.session_id,
            title="New Chat"
        )
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found."
        )

    # Save user message
    save_message(
        db=db,
        session_id=session.id,
        role="user",
        content=user_text
    )

    # Load complete chat history
    history = get_chat_history(db, session.id)

    # Convert history into LLM format
    messages = build_messages(history)

    # Generate assistant response
    assistant_response = generate_response(messages)

    # Save assistant response
    save_message(
        db=db,
        session_id=session.id,
        role="assistant",
        content=assistant_response
    )

    return ChatResponse(
        session_id=session.id,
        response=assistant_response
    )
