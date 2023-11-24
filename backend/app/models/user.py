from beanie import Document, Indexed
from typing import Annotated


class User(Document):
    username: str
    email: str = Annotated[str, Indexed(str, unique=True)]
    favorites: list[int] = []
    read_later: list[int] = []


class UserInDB(User):
    hashed_password: str
