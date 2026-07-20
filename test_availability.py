from app.core.database import SessionLocal

# Load models
from app.modules.auth.models import User
from app.modules.library.models import Book, Loan

from app.modules.library.schemas import CheckAvailabilityRequest
from app.modules.library.tools import check_availability_tool


db = SessionLocal()


request = CheckAvailabilityRequest(
    book_id=5
)


result = check_availability_tool(
    request=request,
    db=db
)


print(result)


db.close()