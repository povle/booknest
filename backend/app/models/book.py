import pymongo
from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Optional, Annotated
from fastapi import HTTPException, Depends, Body


class Book(Document):
    cover: str
    title: Annotated[str, Indexed(index_type=pymongo.TEXT)]
    author: str
    year: int
    genre: str
    description: str
    short_description: str
    rating: int
    original_title: Optional[str] = None
    original_isbn: Optional[str] = None


async def get_book_or_404(book_id: str = Body(..., embed=True)) -> Book:
    book = await Book.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


class PatchBook(BaseModel):
    cover: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    rating: Optional[int] = None


class Rating(Document):
    user_id: str
    isbn: str
    rating: float
