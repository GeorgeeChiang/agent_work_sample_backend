from datetime import date, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine, get_db
from .models import Book, Loan, User
from .schemas import BookOut, BorrowRequest, LoginRequest, LoginResponse, ReturnRequest, UserOut
from .seed import seed

app = FastAPI(title="Library Sample API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or user.password != payload.password:
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    return LoginResponse(user=UserOut(id=user.id, username=user.username, display_name=user.display_name))


@app.get("/users", response_model=list[UserOut])
def users(db: Session = Depends(get_db)) -> list[UserOut]:
    return [UserOut(id=user.id, username=user.username, display_name=user.display_name) for user in db.query(User).order_by(User.id).all()]


@app.get("/books", response_model=list[BookOut])
def books(db: Session = Depends(get_db)) -> list[BookOut]:
    items = db.query(Book).order_by(Book.id).all()
    response: list[BookOut] = []
    for book in items:
        active_loan = next((loan for loan in book.loans if loan.returned_on is None), None)
        response.append(
            BookOut(
                id=book.id,
                title=book.title,
                author=book.author,
                category=book.category,
                status="borrowed" if active_loan else "available",
                borrower=active_loan.user.display_name if active_loan else None,
                borrowed_on=active_loan.borrowed_on if active_loan else None,
                due_on=active_loan.due_on if active_loan else None,
            )
        )
    return response


@app.post("/loans", response_model=BookOut)
def borrow_book(payload: BorrowRequest, db: Session = Depends(get_db)) -> BookOut:
    user = db.query(User).filter(User.username == payload.username).first()
    book = db.query(Book).filter(Book.id == payload.book_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="找不到使用者")
    if book is None:
        raise HTTPException(status_code=404, detail="找不到書籍")
    if any(loan.returned_on is None for loan in book.loans):
        raise HTTPException(status_code=409, detail="此書已被借出")
    today = date.today()
    db.add(Loan(user_id=user.id, book_id=book.id, borrowed_on=today, due_on=today + timedelta(days=14)))
    db.commit()
    db.refresh(book)
    return books(db)[book.id - 1]


@app.post("/loans/{book_id}/return", response_model=BookOut)
def return_book(book_id: int, payload: ReturnRequest, db: Session = Depends(get_db)) -> BookOut:
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="找不到使用者")
    loan = db.query(Loan).filter(Loan.book_id == book_id, Loan.user_id == user.id, Loan.returned_on.is_(None)).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="找不到可歸還的借閱紀錄")
    loan.returned_on = date.today()
    db.commit()
    return books(db)[book_id - 1]
