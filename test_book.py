from app.main import app

from app.core.database import SessionLocal
from app.modules.library.models import Book

db = SessionLocal()

book = db.query(Book).filter(Book.id == 5).first()

print(
    book.title,
    book.available_copies
)

db.close()