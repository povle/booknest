from beanie import Document, Indexed
from typing import Annotated
from .book import Book


class User(Document):
    username: str
    email: str = Annotated[str, Indexed(str, unique=True)]
    favorites: list[Book] = []
    read_later: list[Book] = []
    is_admin: bool = False


class UserInDB(User):
    hashed_password: str
