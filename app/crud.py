from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_users(db: Session):
    return db.query(models.User).all()