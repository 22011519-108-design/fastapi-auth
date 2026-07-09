# FastAPI Authentication System

A basic user authentication system built using FastAPI, SQLAlchemy, and SQLite.

## Features

- User signup API
- Password hashing using bcrypt
- SQLite database integration
- Swagger API documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## How to Run

Install dependencies:

pip install -r requirements.txt

Run server:

uvicorn app.main:app --reload

Open API documentation:

http://127.0.0.1:8000/docs