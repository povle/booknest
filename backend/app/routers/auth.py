from fastapi import Form, APIRouter
from typing import Annotated

router = APIRouter()

@router.post("/register")
async def post_register(username: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        email: Annotated[str, Form()]):
    return {'username': username,
            'password': password,
            'email': email}
