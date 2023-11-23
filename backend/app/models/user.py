from beanie import Document, Indexed
from typing import Annotated


class User(Document):
    username: str
    email: str = Annotated[str, Indexed(str, unique=True)]


class UserInDB(User):
    hashed_password: str
