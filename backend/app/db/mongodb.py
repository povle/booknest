from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import UserInDB

client = AsyncIOMotorClient("mongodb://mongo:27017")


async def init_db():
    return await init_beanie(database=client.booknest,
                             document_models=[UserInDB])
