from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.library.tools import dashboard_stats_tool
from app.modules.library.schemas import (
    SearchBooksRequest,
    CheckAvailabilityRequest,
    BorrowBookRequest,
    ReturnBookRequest,
)

from app.modules.library.tools import (
    search_books_tool,
    check_availability_tool,
    borrow_book_tool,
    return_book_tool,
    dashboard_stats_tool,
)

router = APIRouter(
    prefix="/library",
    tags=["Library"]
)


@router.post("/search")
def search_books(
    request: SearchBooksRequest,
    db: Session = Depends(get_db)
):
    return search_books_tool(request, db)


@router.post("/check")
def check_availability(
    request: CheckAvailabilityRequest,
    db: Session = Depends(get_db)
):
    return check_availability_tool(request, db)


@router.post("/borrow")
def borrow_book(
    request: BorrowBookRequest,
    db: Session = Depends(get_db)
):
    return borrow_book_tool(request, db)


@router.post("/return")
def return_book(
    request: ReturnBookRequest,
    db: Session = Depends(get_db)
):
    return return_book_tool(request, db)

@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):
    return dashboard_stats_tool(db)