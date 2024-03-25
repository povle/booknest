from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import UserInDB, Book, Rating
from .dataset import load_datasets

client = AsyncIOMotorClient("mongodb://mongo:27017")


async def init_db():
    res = await init_beanie(database=client.booknest,
                            document_models=[UserInDB, Book, Rating])
    books, ratings = load_datasets()
    await Book.insert_many(books)
    await Rating.insert_many(ratings)
    return res
