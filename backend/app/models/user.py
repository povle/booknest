from beanie import Document, Indexed
from typing import Annotated, Optional
from pydantic import BaseModel
from .book import Book


class User(Document):
    username: str
    email: str = Annotated[str, Indexed(str, unique=True)]
    favorites: list[Book] = []
    read_later: list[Book] = []
    is_admin: bool = False


class PatchUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserInDB(User):
    hashed_password: str
