from app.main import app

from app.core.database import SessionLocal
from app.modules.auth.models import User

db = SessionLocal()

users = db.query(User).all()

for user in users:
    print(
        f"ID={user.id}, Username={user.username}, Email={user.email}"
    )

db.close()