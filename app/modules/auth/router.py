from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.modules.auth import service
from app.modules.auth.schemas import UserCreate, UserLogin
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

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
    form_data: OAuth2PasswordRequestForm = Depends()
):
    email = form_data.username
    password = form_data.password

    # yahan tum apni existing login verification call karo

    token = create_access_token(
        data={"sub": email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }