from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.modules.auth import service
from app.modules.auth.schemas import UserCreate, UserLogin

router = APIRouter(tags=["Authentication"])


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return service.signup(user, db)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return service.login(user, db)


@router.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
    return {
        "message": "Protected route accessed",
        "user": current_user
    }


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return service.login_with_form(
        username=form_data.username,
        password=form_data.password,
        db=db
    )
