import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:2811@localhost:5432/fastapi_db"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "my-super-secret-key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30