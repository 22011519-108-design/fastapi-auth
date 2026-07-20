from app.core.database import SessionLocal

# Load all models first
from app.modules.auth.models import User
from app.modules.library.models import Book, Loan

from app.modules.library.schemas import SearchBooksRequest
from app.modules.library.tools import search_books_tool


db = SessionLocal()

request = SearchBooksRequest(
    query="python"
)

result = search_books_tool(
    request=request,
    db=db
)

print(result)

db.close()