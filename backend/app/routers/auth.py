from fastapi import Form, APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.models import User, UserInDB, Token
from app.utils import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, get_password_hash, get_user
from datetime import timedelta

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
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
