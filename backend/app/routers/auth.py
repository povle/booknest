from fastapi import Form, APIRouter, HTTPException
from typing import Annotated
from app.models import User
from app.db import db

router = APIRouter()


@router.post("/register")
async def post_register(username: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        email: Annotated[str, Form()]):
    user = await db.find_one(User, User.email == email)
    if user:
        raise HTTPException(status_code=409, detail="Email already exists")
    user = User(username=username, password=password, email=email)
    await db.save(user)
    return user
