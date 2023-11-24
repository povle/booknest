from fastapi import Form, APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from typing import Annotated
from app.models import User, UserInDB, Token
from app.utils import (get_current_user,
                       get_password_hash,
                       get_user,
                       get_token,
                       ACCESS_TOKEN_EXPIRE_MINUTES)

router = APIRouter()


@router.post("/register")
async def post_register(username: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        email: Annotated[str, Form()]):
    user = await get_user(email)
    if user is not None:
        raise HTTPException(
            status_code=409,
            detail='User with this email already exists')

    user = UserInDB(username=username,
                    hashed_password=get_password_hash(password),
                    email=email)
    await user.insert()

    response = RedirectResponse(url='/login.html', status_code=status.HTTP_302_FOUND)
    return response


@router.post("/token", response_model=Token)
async def login_for_access_token(access_token: str = Depends(get_token)):
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(access_token: str = Depends(get_token)):
    response = RedirectResponse(url='/app/recommended.html', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key='Authorization',
                        value=f'Bearer {access_token}',
                        httponly=True,
                        samesite='strict',
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url='/login.html', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='Authorization')
    return response


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
