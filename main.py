from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends
from starlette.responses import FileResponse

from db import models
from routes import mountains, production_only, users, achievements, qr, ranking, collection, comments
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine

app = FastAPI()
router = APIRouter()

# models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://koronagorpolskich.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(mountains.router, tags=['Mountains'], prefix='/api/mountains')
app.include_router(users.router, tags=['Users'], prefix='')
app.include_router(achievements.router, tags=['Achievements'], prefix='/achievements')
app.include_router(qr.router, tags=['QR'], prefix='/qr')
app.include_router(ranking.router, tags=['Ranking'], prefix='/ranking')
app.include_router(collection.router, tags=['Kolekcja'], prefix='/collection')
app.include_router(comments.router, tags=['Komentarze'], prefix='/comments')

# app.include_router(production_only.router, tags=['Production tests'], prefix='/test')

@app.get('/mountains_img/{image_name}')
def getImage(image_name: str):
    return FileResponse(f'mountains_img/{image_name}')