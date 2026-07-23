from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.library.models import Book, Loan


def search_books(db: Session, query: str):
    """
    Search books by title, author, or genre.
    """
    books = (
        db.query(Book)
        .filter(
            or_(
                Book.title.ilike(f"%{query}%"),
                Book.author.ilike(f"%{query}%"),
                Book.genre.ilike(f"%{query}%")
            )
        )
        .all()
    )

    return books


def check_availability(db: Session, book_id: int):
    """
    Check if a book is available.
    """
    return (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )


def borrow_book(
    db: Session,
    user_id: int,
    book_id: int
):
    """
    Borrow a book.
    """

    # Check user
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    # Check book
    book = (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )

    if not book:
        return {
            "success": False,
            "message": "Book not found."
        }

    # Check availability
    if book.available_copies <= 0:
        return {
            "success": False,
            "message": "Book is not available."
        }

    # Check if already borrowed
    existing_loan = (
        db.query(Loan)
        .filter(
            Loan.user_id == user_id,
            Loan.book_id == book_id,
            Loan.status == "borrowed"
        )
        .first()
    )

    if existing_loan:
        return {
            "success": False,
            "message": "You have already borrowed this book."
        }

    # Check borrowing limit
    active_loans = (
        db.query(Loan)
        .filter(
            Loan.user_id == user_id,
            Loan.status == "borrowed"
        )
        .count()
    )

    if active_loans >= 3:
        return {
            "success": False,
            "message": "Maximum borrowing limit reached (3 books)."
        }

    # Create loan
    loan = Loan(
        user_id=user_id,
        book_id=book_id,
        borrowed_at=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14),
        status="borrowed"
    )

    try:
        db.add(loan)

        # Decrease available copies
        book.available_copies -= 1

        db.commit()
        db.refresh(loan)

        return {
            "success": True,
            "message": "Book borrowed successfully.",
            "loan_id": loan.id,
            "book": book.title,
            "due_date": loan.due_date
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": f"Error borrowing book: {str(e)}"
        }


def return_book(
    db: Session,
    loan_id: int
):
    """
    Return a borrowed book.
    """

    loan = (
        db.query(Loan)
        .filter(Loan.id == loan_id)
        .first()
    )

    if not loan:
        return {
            "success": False,
            "message": "Loan not found."
        }

    if loan.status == "returned":
        return {
            "success": False,
            "message": "Book has already been returned."
        }

    book = (
        db.query(Book)
        .filter(Book.id == loan.book_id)
        .first()
    )

    try:
        loan.status = "returned"
        loan.returned_at = datetime.utcnow()

        book.available_copies += 1

        db.commit()

        return {
            "success": True,
            "message": "Book returned successfully.",
            "book": book.title
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": f"Error returning book: {str(e)}"
        }

def get_my_borrowed_books(
    db: Session,
    user_id: int
):
    """
    Get all active borrowed books for a user.
    """

    loans = (
        db.query(Loan)
        .filter(
            Loan.user_id == user_id,
            Loan.status == "borrowed"
        )
        .all()
    )

    if not loans:
        return []

    borrowed_books = []

    for loan in loans:
        borrowed_books.append(
            {
                "loan_id": loan.id,
                "book_id": loan.book.id,
                "title": loan.book.title,
                "author": loan.book.author,
                "due_date": loan.due_date,
                "borrowed_at": loan.borrowed_at,
            }
        )

    return borrowed_books       


def get_dashboard_stats(db: Session):

    total_books = db.query(Book).count()

    total_users = db.query(User).count()

    borrowed = (
        db.query(Loan)
        .filter(Loan.status == "borrowed")
        .count()
    )

    available = (
        db.query(Book.available_copies)
        .all()
    )

    available = sum(book[0] for book in available)

    return {
        "total_books": total_books,
        "total_users": total_users,
        "borrowed_books": borrowed,
        "available_books": available
    }