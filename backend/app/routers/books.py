from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.utils import get_current_user, get_admin_user, find_in_links
from app.models import Book, PatchBook, User
from typing import List
from beanie.operators import In
from app.models.book import get_book_or_404


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
    return await get_book_or_404(book_id)


@router.post('/books', response_model=Book)
async def post_book(book: Book, _=Depends(get_admin_user)):
    inserted = await book.insert()
    return inserted


@router.patch('/books/{book_id}', response_model=Book)
async def patch_book(book_id: str, updates: PatchBook, _=Depends(get_admin_user)):
    book = await get_book_or_404(book_id)
    await book.update({"$set": updates.model_dump(exclude_unset=True, exclude=['id'])})
    return book


@router.get('/recommended')
async def get_recommended(_=Depends(get_current_user)):
    return RedirectResponse(url='books')  # FIXME


@router.get('/favorites')
async def get_favorites(user=Depends(get_current_user)):
    await user.fetch_link(User.favorites)
    return user.favorites


@router.post('/favorites')
async def post_favorites(book=Depends(get_book_or_404), user=Depends(get_current_user)):
    user.favorites.append(book)
    await user.save()
    return True


@router.post('/favorites/toggle')
async def toggle_favorites(book=Depends(get_book_or_404), user=Depends(get_current_user)):
    found = find_in_links(user.favorites, book)
    if found:
        user.favorites.remove(found)
        await user.save()
        return False
    else:
        user.favorites.append(book)
        await user.save()
        return True


@router.delete('/favorites')
async def delete_favorites(book=Depends(get_book_or_404), user=Depends(get_current_user)):
    found = find_in_links(user.favorites, book)
    if not found:
        return False
    user.favorites.remove(found)
    await user.save()
    return False


@router.get('/read_later')
async def get_read_later(user=Depends(get_current_user)):
    await user.fetch_link(User.read_later)
    return user.read_later


@router.post('/read_later')
async def post_read_later(book=Depends(get_book_or_404), user=Depends(get_current_user)):
    user.read_later.append(book)
    await user.save()
    return True


@router.delete('/read_later')
async def delete_read_later(book=Depends(get_book_or_404), user=Depends(get_current_user)):
    found = find_in_links(user.read_later, book)
    if not found:
        return False
    user.read_later.remove(found)
    await user.save()
    return False


@router.post('/read_later/toggle')
async def toggle_read_later(book=Depends(get_book_or_404), user=Depends(get_current_user)):
    found = find_in_links(user.read_later, book)
    if found:
        user.read_later.remove(found)
        await user.save()
        return False
    else:
        user.read_later.append(book)
        await user.save()
        return True
