from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse
from app.utils import get_current_user, get_admin_user
from app.models import Book, PatchBook
from typing import List
from beanie.operators import In


router = APIRouter()


@router.get('/books', response_model=List[Book])
async def get_books(q: str = None, _=Depends(get_current_user)):
    if q:
        return await Book.find_many(
            In(Book.title, q.split(' '))
        ).to_list()
    return await Book.find_all().to_list()


@router.get('/books/{book_id}', response_model=Book)
async def get_book(book_id: str, _=Depends(get_current_user)):
    return await Book.get(book_id)


@router.post('/books', response_model=Book)
async def post_book(book: Book, _=Depends(get_admin_user)):
    inserted = await book.insert()
    return inserted


@router.patch('/books/{book_id}', response_model=Book)
async def patch_book(book_id: str, updates: PatchBook, _=Depends(get_admin_user)):
    print(updates)
    book = await Book.get(book_id)
    await book.update({"$set": updates.model_dump(exclude_unset=True, exclude=['id'])})
    return book


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
