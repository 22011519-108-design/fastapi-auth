from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.users import service

router = APIRouter(tags=["Users"])

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return service.get_users(db)


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(user_id, db)