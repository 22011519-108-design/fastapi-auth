from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.modules.auth.models import User
from app.modules.library.models import Book


def seed_books():
    db: Session = SessionLocal()

    # Don't seed twice
    if db.query(Book).count() > 0:
        print("Books already exist.")
        db.close()
        return

    books = [
        Book(title="Clean Code", author="Robert C. Martin", genre="Programming", total_copies=5, available_copies=3),
        Book(title="The Pragmatic Programmer", author="Andrew Hunt", genre="Programming", total_copies=4, available_copies=2),
        Book(title="Design Patterns", author="GoF", genre="Programming", total_copies=3, available_copies=1),
        Book(title="Introduction to Algorithms", author="Cormen", genre="Computer Science", total_copies=2, available_copies=0),
        Book(title="Python Crash Course", author="Eric Matthes", genre="Programming", total_copies=6, available_copies=6),
        Book(title="Deep Learning", author="Ian Goodfellow", genre="AI", total_copies=3, available_copies=2),
        Book(title="Artificial Intelligence: A Modern Approach", author="Russell & Norvig", genre="AI", total_copies=2, available_copies=1),
        Book(title="Atomic Habits", author="James Clear", genre="Self Help", total_copies=5, available_copies=5),
        Book(title="The Psychology of Money", author="Morgan Housel", genre="Finance", total_copies=4, available_copies=4),
        Book(title="The Alchemist", author="Paulo Coelho", genre="Novel", total_copies=3, available_copies=3),
        Book(title="1984", author="George Orwell", genre="Novel", total_copies=5, available_copies=2),
        Book(title="To Kill a Mockingbird", author="Harper Lee", genre="Novel", total_copies=4, available_copies=1),
    ]

    db.add_all(books)
    db.commit()
    db.close()

    print("Books seeded successfully!")


if __name__ == "__main__":
    seed_books()