from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models
from .security import hash_password, verify_password


def create_user(db: Session, user):

    # Check if username or email already exists
    existing_user = db.query(models.User).filter(
        or_(
            models.User.username == user.username,
            models.User.email == user.email
        )
    ).first()

    if existing_user:
        return None

    # Create new user
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, username_or_email, password):

    user = db.query(models.User).filter(
        or_(
            models.User.username == username_or_email,
            models.User.email == username_or_email
        )
    ).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()