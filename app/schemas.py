from datetime import date

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    display_name: str


class LoginResponse(BaseModel):
    user: UserOut


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    category: str
    status: str
    borrower: str | None
    borrowed_on: date | None
    due_on: date | None


class BorrowRequest(BaseModel):
    username: str
    book_id: int | None = None
