from sqlalchemy.orm import Session

from app.modules.auth.models import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, hashed_password: str):

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session):
    return db.query(User).all()