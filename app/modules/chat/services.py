import logging
import time
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import GROQ_API_KEY, GROQ_MODEL
from app.modules.chat.models import ChatMessage, ChatSession

try:
    from groq import Groq
except ImportError:
    Groq = None

logger = logging.getLogger(__name__)

AI_UNAVAILABLE_MESSAGE = (
    "Sorry, the AI service is temporarily unavailable. "
    "Please try again later."
)

_groq_client: Any | None = None

SYSTEM_PROMPT = """
You are a helpful AI assistant.

Instructions:
- Answer clearly and accurately.
- Be polite and professional.
- Maintain conversation context.
- If you don't know the answer, say so instead of guessing.
"""


def get_or_create_session(
    db: Session,
    user_id: int,
    session_id: int | None = None,
    title: str = "New Chat"
) -> ChatSession:
    if session_id is not None:
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id
            )
            .first()
        )

        if session is None:
            raise ValueError("Chat session not found")

        return session

    session = ChatSession(
        user_id=user_id,
        title=title
    )

    db.add(session)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(session)

    return session


def get_latest_or_create_session(
    db: Session,
    user_id: int,
    title: str = "WebSocket Chat"
) -> ChatSession:
    session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc(), ChatSession.id.desc())
        .first()
    )

    if session is not None:
        return session

    return get_or_create_session(
        db=db,
        user_id=user_id,
        title=title
    )


def save_message(
    db: Session,
    session_id: int,
    role: str,
    content: str
) -> ChatMessage:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(message)

    return message


def get_chat_history(db: Session, session_id: int) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at, ChatMessage.id)
        .all()
    )


def serialize_history(history: list[ChatMessage]) -> list[dict[str, str]]:
    return [
        {
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at.isoformat()
            if message.created_at
            else ""
        }
        for message in history
    ]


def build_messages(history: list[ChatMessage]) -> list[dict]:
    """
    Convert chat history into LLM message format.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for msg in history:
        messages.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )

    return messages


def get_groq_client():
    global _groq_client

    if Groq is None:
        raise RuntimeError("groq package is not installed")

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY environment variable is required")

    if _groq_client is None:
        _groq_client = Groq(api_key=GROQ_API_KEY)

    return _groq_client

def moderate_input(user_input: str) -> tuple[bool, str]:
    """
    Perform a basic moderation check on user input.

    Returns:
        (True, "") if the message is safe.
        (False, reason) if the message should be blocked.
    """

    blocked_keywords = [
        "kill myself",
        "suicide",
        "bomb",
        "terrorist",
        "murder",
        "child abuse",
    ]

    text = user_input.lower()

    for keyword in blocked_keywords:
        if keyword in text:
            return (
                False,
                "Your message violates the application's safety policy."
            )

    return True, ""

def generate_response(messages: list[dict]) -> str:
    """
    Generate AI response using Groq.
    """

    # Check the latest user message before sending it to the LLM
    user_message = ""

    for message in reversed(messages):
        if message["role"] == "user":
            user_message = message["content"]
            break

    is_safe, moderation_message = moderate_input(user_message)

    if not is_safe:
        logger.warning(
            "Blocked unsafe user input: %s",
            user_message
        )
        return moderation_message

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = get_groq_client().chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            if not response.choices:
                raise RuntimeError("Groq returned no choices")

            content = response.choices[0].message.content

            if not content:
                raise RuntimeError("Groq returned an empty response")

            usage = getattr(response, "usage", None)

            if usage:
                logger.info(
                    "Groq usage: prompt=%s completion=%s total=%s",
                    getattr(usage, "prompt_tokens", None),
                    getattr(usage, "completion_tokens", None),
                    getattr(usage, "total_tokens", None),
                )

            return content.strip()

        except Exception as e:

            logger.warning(
                "Groq request attempt %s/%s failed: %s",
                attempt + 1,
                max_attempts,
                e,
                exc_info=attempt == max_attempts - 1
            )

            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt)

    return AI_UNAVAILABLE_MESSAGE