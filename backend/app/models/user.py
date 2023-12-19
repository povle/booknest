from beanie import Document, Indexed, Link
from typing import Annotated, Optional, List
from pydantic import BaseModel
from .book import Book


class User(Document):
    username: str
    email: str = Annotated[str, Indexed(str, unique=True)]
    favorites: List[Link[Book]] = []
    read_later: List[Link[Book]] = []
    is_admin: bool = False


class PatchUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserInDB(User):
    hashed_password: str
