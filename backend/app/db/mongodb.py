from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient

db = AIOEngine(client=AsyncIOMotorClient("mongodb://mongo:27017"))
