from sqlalchemy.orm import Session

from app.modules.library.schemas import SearchBooksRequest
from app.modules.library.schemas import CheckAvailabilityRequest
from app.modules.library import services
from app.modules.library.schemas import BorrowBookRequest
from app.modules.library.schemas import ReturnBookRequest

def search_books_tool(request: SearchBooksRequest, db: Session):
    """
    Tool: Search books in the library.
    """

    books = services.search_books(
        db=db,
        query=request.query
    )

    if not books:
        return {
            "message": "No matching books found.",
            "books": []
        }

    return {
        "message": "Books found.",
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "available_copies": book.available_copies
            }
            for book in books
        ]
    }

def check_availability_tool(
    request: CheckAvailabilityRequest,
    db: Session
):
    """
    Tool: Check book availability.
    """

    book = services.check_availability(
        db=db,
        book_id=request.book_id
    )

    if not book:
        return {
            "message": "Book not found.",
            "available": False
        }

    return {
        "book_id": book.id,
        "title": book.title,
        "available_copies": book.available_copies,
        "available": book.available_copies > 0
    }

def borrow_book_tool(
    request: BorrowBookRequest,
    db: Session
):
    """
    Tool: Borrow a book.
    """

    result = services.borrow_book(
        db=db,
        user_id=request.user_id,
        book_id=request.book_id
    )

    return result

def return_book_tool(
    request: ReturnBookRequest,
    db: Session
):
    """
    Tool: Return a borrowed book.
    """

    return services.return_book(
        db=db,
        loan_id=request.loan_id
    )

def dashboard_stats_tool(db: Session):

    return services.get_dashboard_stats(db)