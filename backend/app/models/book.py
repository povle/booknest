from beanie import Document
from pydantic import BaseModel
from typing import Optional

class Book(Document):
    cover: str
    title: str
    author: str
    year: int
    genre: str
    description: str
    short_description: str
    rating: int


class OptionalBook(BaseModel):
    cover: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    rating: Optional[int] = None
