from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate, UserLogin
from app.modules.auth import repository
from app.core.security import hash_password, verify_password, create_access_token


def signup(user: UserCreate, db: Session):

    existing_user = repository.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = repository.create_user(
        db=db,
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    return {
        "message": "User created successfully",
        "user": new_user
    }


def login(user: UserLogin, db: Session):

    db_user = repository.get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }