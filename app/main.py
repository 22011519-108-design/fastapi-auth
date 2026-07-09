from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import schemas, crud

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Authentication API")


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Signup Endpoint
@app.post("/signup")
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)

    if new_user is None:
        raise HTTPException(
            status_code=400,
            detail="Username or Email already exists"
        )

    return {"message": "User created successfully"}


# Login Endpoint
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(
        db,
        user.username_or_email,
        user.password
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username/email or password"
        )

    return {
        "access_token": "dummy_token_12345",
        "token_type": "bearer"
    }


# Get User Endpoint
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user