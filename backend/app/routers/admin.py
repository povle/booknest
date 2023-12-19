from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.utils import get_admin_user
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='frontend/templates')

router = APIRouter(dependencies=[Depends(get_admin_user)])


@router.get('/edit_book.html', response_class=HTMLResponse)
async def get_edit_book(request: Request):
    return templates.TemplateResponse('edit_book.html', context={'request': request})
