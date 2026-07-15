from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime

from app.core.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)

    role = Column(String, nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)