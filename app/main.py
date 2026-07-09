from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, SessionLocal


# Database tables create
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home route
@app.get("/")
def home():
    return {"message": "FastAPI Auth API Running"}


# Signup API
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


# Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None:
        return {"message": "User not found"}

    return user