from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.chat.schemas import ChatRequest, ChatResponse
from app.modules.chat.models import ChatSession, ChatMessage

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    # Agar session_id nahi aayi to naya session banao
    if request.session_id is None:
        session = ChatSession(
            user_id=1,
            title="New Chat"
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        # User message save karo
        message = ChatMessage(
            session_id=session.id,
            role="user",
            content=request.message
        )

        db.add(message)
        db.commit()

        return ChatResponse(
            session_id=session.id,
            response="New chat session created!"
        )

    return ChatResponse(
        session_id=request.session_id,
        response="Existing session"
    )