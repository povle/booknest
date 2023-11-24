from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse, FileResponse
from app.utils import get_current_user


router = APIRouter()


@router.get('/books')
async def get_books(user=Depends(get_current_user)):
    return FileResponse('frontend/unprotected/assets/books.json')  # FIXME


@router.get('/recommended')
async def get_recommended(user=Depends(get_current_user)):
    return RedirectResponse(url='books')  # FIXME


@router.get('/favorites')
async def get_favorites(user=Depends(get_current_user)):
    return user.favorites


@router.post('/favorites')
async def post_favorites(book_id: int = Body(..., embed=True), user=Depends(get_current_user)):
    if book_id in user.favorites:
        return True
    user.favorites.append(book_id)
    await user.save()
    return True


@router.post('/favorites/toggle')
async def toggle_favorites(book_id: int = Body(..., embed=True), user=Depends(get_current_user)):
    if book_id in user.favorites:
        user.favorites.remove(book_id)
        await user.save()
        return False
    else:
        user.favorites.append(book_id)
        await user.save()
        return True


@router.delete('/favorites')
async def delete_favorites(book_id: int = Body(..., embed=True), user=Depends(get_current_user)):
    if book_id not in user.favorites:
        return False
    user.favorites.remove(book_id)
    await user.save()
    return False


@router.get('/read_later')
async def get_read_later(user=Depends(get_current_user)):
    return user.read_later


@router.post('/read_later')
async def post_read_later(book_id: int = Body(..., embed=True), user=Depends(get_current_user)):
    if book_id in user.read_later:
        return True
    user.read_later.append(book_id)
    await user.save()
    return True


@router.delete('/read_later')
async def delete_read_later(book_id: int = Body(..., embed=True), user=Depends(get_current_user)):
    if book_id not in user.read_later:
        return False
    user.read_later.remove(book_id)
    await user.save()
    return False


@router.post('/read_later/toggle')
async def toggle_read_later(book_id: int = Body(..., embed=True), user=Depends(get_current_user)):
    if book_id in user.read_later:
        user.read_later.remove(book_id)
        await user.save()
        return False
    else:
        user.read_later.append(book_id)
        await user.save()
        return True
