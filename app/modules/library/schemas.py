from pydantic import BaseModel


class SearchBooksRequest(BaseModel):
    query: str


class CheckAvailabilityRequest(BaseModel):
    book_id: int


class BorrowBookRequest(BaseModel):
    user_id: int
    book_id: int


class ReturnBookRequest(BaseModel):
    user_id: int
    book_id: int


class GetBorrowedBooksRequest(BaseModel):
    user_id: int

class CheckAvailabilityRequest(BaseModel):
    book_id: int

class BorrowBookRequest(BaseModel):
    user_id: int
    book_id: int

class ReturnBookRequest(BaseModel):
    loan_id: int