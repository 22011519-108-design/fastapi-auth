from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.users import repository


def get_users(db: Session):
    return repository.get_all_users(db)


def get_user(user_id: int, db: Session):

    user = repository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user