from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.modules.auth.models import User
from app.modules.library.models import Book
from app.modules.rag.services import index_document


def seed_books():
    db: Session = SessionLocal()

    # Don't seed twice
    if db.query(Book).count() > 0:
        print("Books already exist.")
        db.close()
        return

    books = [
        Book(
            title="Clean Code",
            author="Robert C. Martin",
            genre="Programming",
            description="A guide to writing clean, maintainable, and readable code. Covers SOLID principles, refactoring, code smells, and software craftsmanship.",
            total_copies=5,
            available_copies=3,
        ),
        Book(
            title="The Pragmatic Programmer",
            author="Andrew Hunt",
            genre="Programming",
            description="A practical guide to becoming a better software developer through best practices, problem solving, and continuous learning.",
            total_copies=4,
            available_copies=2,
        ),
        Book(
            title="Design Patterns",
            author="GoF",
            genre="Programming",
            description="Explains reusable object-oriented design patterns such as Singleton, Factory, Observer, and Strategy.",
            total_copies=3,
            available_copies=1,
        ),
        Book(
            title="Introduction to Algorithms",
            author="Cormen",
            genre="Computer Science",
            description="Comprehensive coverage of algorithms, data structures, graph algorithms, sorting, searching, and dynamic programming.",
            total_copies=2,
            available_copies=0,
        ),
        Book(
            title="Python Crash Course",
            author="Eric Matthes",
            genre="Programming",
            description="A beginner-friendly guide to Python covering variables, loops, functions, classes, file handling, and real-world projects.",
            total_copies=6,
            available_copies=6,
        ),
        Book(
            title="Deep Learning",
            author="Ian Goodfellow",
            genre="AI",
            description="Explains neural networks, deep learning algorithms, convolutional neural networks, recurrent neural networks, and machine learning concepts.",
            total_copies=3,
            available_copies=2,
        ),
        Book(
            title="Artificial Intelligence: A Modern Approach",
            author="Russell & Norvig",
            genre="AI",
            description="A comprehensive introduction to artificial intelligence, including search algorithms, knowledge representation, reasoning, planning, and machine learning.",
            total_copies=2,
            available_copies=1,
        ),
        Book(
            title="Atomic Habits",
            author="James Clear",
            genre="Self Help",
            description="Teaches habit formation, productivity, personal growth, and how small daily improvements lead to long-term success.",
            total_copies=5,
            available_copies=5,
        ),
        Book(
            title="The Psychology of Money",
            author="Morgan Housel",
            genre="Finance",
            description="Explores personal finance, investing, wealth building, financial behavior, and decision-making with real-life examples.",
            total_copies=4,
            available_copies=4,
        ),
        Book(
            title="The Alchemist",
            author="Paulo Coelho",
            genre="Novel",
            description="A philosophical novel about following dreams, discovering purpose, and listening to one's heart.",
            total_copies=3,
            available_copies=3,
        ),
        Book(
            title="1984",
            author="George Orwell",
            genre="Novel",
            description="A dystopian novel exploring surveillance, totalitarianism, censorship, and loss of individual freedom.",
            total_copies=5,
            available_copies=2,
        ),
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre="Novel",
            description="A classic novel about justice, racism, compassion, morality, and childhood in the American South.",
            total_copies=4,
            available_copies=1,
        ),
    ]

    db.add_all(books)
    db.commit()

    # Refresh objects to ensure they have database IDs
    for book in books:
        db.refresh(book)

    # Index books into FAISS
    for book in books:
        index_document(
            title=book.title,
            text=book.description or "",
        )

    db.close()

    print("Books seeded and indexed successfully!")


if __name__ == "__main__":
    seed_books()