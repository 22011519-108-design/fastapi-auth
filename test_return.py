from app.main import app

from app.core.database import SessionLocal

from app.modules.library.schemas import ReturnBookRequest
from app.modules.library.tools import return_book_tool

db = SessionLocal()

request = ReturnBookRequest(
    loan_id=1
)

result = return_book_tool(
    request=request,
    db=db
)

print(result)

db.close()