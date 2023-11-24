from fastapi import Form, APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Annotated
from app.models import User, UserInDB, Token
from app.utils import (get_current_user,
                       get_password_hash,
                       get_user,
                       get_token,
                       get_token_or_none,
                       ACCESS_TOKEN_EXPIRE_MINUTES,
                       redirect_if_authenticated)
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend/templates')

router = APIRouter()


@router.get('/register.html', response_class=HTMLResponse)
async def get_register(request: Request, _=Depends(redirect_if_authenticated)):
    return templates.TemplateResponse('register.html', context={'request': request})


@router.post('/register.html')
async def post_register(request: Request,
                        username: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        email: Annotated[str, Form()],
                        _=Depends(redirect_if_authenticated)):
    user = await get_user(email)
    if user is not None:
        return templates.TemplateResponse('register.html',
                                          context={'error_message': 'Пользователь с таким email уже существует',
                                                   'request': request})

    user = UserInDB(username=username,
                    hashed_password=get_password_hash(password),
                    email=email)
    await user.insert()

    response = RedirectResponse(url='/login.html', status_code=status.HTTP_302_FOUND)
    return response


@router.get('/login.html', response_class=HTMLResponse)
async def get_login(request: Request, _=Depends(redirect_if_authenticated)):
    return templates.TemplateResponse('login.html', context={'request': request})


@router.post('/login.html')
async def login(request: Request,
                access_token: str = Depends(get_token_or_none),
                _=Depends(redirect_if_authenticated)):
    if access_token is None:
        return templates.TemplateResponse('login.html',
                                          context={'error_message': 'Неверный логин или пароль',
                                                   'request': request})
    response = RedirectResponse(url='/app/recommended.html', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key='Authorization',
                        value=f'Bearer {access_token}',
                        httponly=True,
                        samesite='strict',
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return response


@router.get('/', response_class=HTMLResponse)
@router.get('/index.html', response_class=HTMLResponse)
async def index(request: Request, _=Depends(redirect_if_authenticated)):
    return templates.TemplateResponse('index.html', context={'request': request})


@router.get('/logout')
async def logout():
    response = RedirectResponse(url='/login.html', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='Authorization')
    return response


@router.post('/token', response_model=Token)
async def login_for_access_token(access_token: str = Depends(get_token)):
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me/', response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
