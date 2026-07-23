from sqlalchemy.orm import Session

from app.modules.library.tools import (
    search_books_tool,
    check_availability_tool,
    borrow_book_tool,
    return_book_tool,
    get_my_borrowed_books_tool,
)

from app.modules.library.schemas import (
    SearchBooksRequest,
    CheckAvailabilityRequest,
    BorrowBookRequest,
    ReturnBookRequest,
    GetBorrowedBooksRequest,
)


def run_catalog_agent(
    tool_name: str,
    arguments: dict,
    db: Session
):
    """
    Catalog Agent.

    Responsible for:
    - searching books
    - checking availability
    - borrowing books
    - returning books
    - viewing borrowed books
    """

    tools = {
        "search_books": search_books_tool,
        "check_availability": check_availability_tool,
        "borrow_book": borrow_book_tool,
        "return_book": return_book_tool,
        "get_my_borrowed_books": get_my_borrowed_books_tool,
    }


    tool = tools.get(tool_name)


    if tool is None:
        return {
            "success": False,
            "message": "Unknown catalog operation."
        }


    # Convert dictionary arguments into Pydantic request models

    if tool_name == "search_books":

        arguments = SearchBooksRequest(
            **arguments
        )


    elif tool_name == "check_availability":

        arguments = CheckAvailabilityRequest(
            **arguments
        )


    elif tool_name == "borrow_book":

        arguments = BorrowBookRequest(
            **arguments
        )


    elif tool_name == "return_book":

        arguments = ReturnBookRequest(
            **arguments
        )


    elif tool_name == "get_my_borrowed_books":

        arguments = GetBorrowedBooksRequest(
            **arguments
        )


    return tool(
        request=arguments,
        db=db
    )