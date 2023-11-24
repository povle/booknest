from app.routers import auth, books
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db import init_db
from app.utils import AuthStaticFiles

app = FastAPI()

app.add_event_handler('startup', init_db)
app.include_router(auth.router)
app.include_router(books.router, prefix='/api')

app.mount('/app', AuthStaticFiles(directory='frontend/protected', html=True), name='protected')
app.mount('/', StaticFiles(directory='frontend/unprotected', html=True), name='frontend')
