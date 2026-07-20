from app.main import app

from app.core.database import SessionLocal

from app.modules.library.schemas import BorrowBookRequest
from app.modules.library.tools import borrow_book_tool

db = SessionLocal()

request = BorrowBookRequest(
    user_id=1,
    book_id=5
)

result = borrow_book_tool(
    request=request,
    db=db
)

print(result)

db.close()