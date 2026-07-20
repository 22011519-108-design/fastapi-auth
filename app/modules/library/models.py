from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)

    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    loans = relationship("Loan", back_populates="book")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)

    returned_at = Column(DateTime, nullable=True)

    status = Column(String, default="borrowed")

    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")