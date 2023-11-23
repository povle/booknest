from app.routers import auth
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db import init_db

app = FastAPI()

app.add_event_handler("startup", init_db)
app.include_router(auth.router)
app.mount('/', StaticFiles(directory='frontend', html=True), name='frontend')
