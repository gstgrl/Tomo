# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routes import reserch
from app.routes import user
from app.routes import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # indirizzo frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reserch.router, prefix='/research')
app.include_router(user.router, prefix='/user')
app.include_router(database.router, prefix='/database')


