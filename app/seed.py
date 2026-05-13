from datetime import date, timedelta

from sqlalchemy.orm import Session

from .models import Book, Loan, User


BOOKS = [
    ("Clean Code", "Robert C. Martin", "Engineering"),
    ("Domain-Driven Design", "Eric Evans", "Engineering"),
    ("Refactoring", "Martin Fowler", "Engineering"),
    ("Design of Everyday Things", "Don Norman", "UX"),
    ("Inspired", "Marty Cagan", "Product"),
    ("Lean UX", "Jeff Gothelf", "UX"),
    ("The Pragmatic Programmer", "Andrew Hunt", "Engineering"),
    ("Continuous Delivery", "Jez Humble", "DevOps"),
    ("Hooked", "Nir Eyal", "Product"),
    ("Sprint", "Jake Knapp", "Product"),
]


def seed(db: Session) -> None:
    if db.query(User).count() > 0:
        return

    users = [
        User(username="user1", display_name="小明", password="123456"),
        User(username="user2", display_name="小華", password="123456"),
        User(username="user3", display_name="小美", password="123456"),
    ]
    db.add_all(users)
    db.flush()

    books = [Book(title=title, author=author, category=category) for title, author, category in BOOKS]
    db.add_all(books)
    db.flush()

    today = date.today()
    db.add(
        Loan(
            user_id=users[0].id,
            book_id=books[0].id,
            borrowed_on=today,
            due_on=today + timedelta(days=14),
        )
    )
    db.commit()

