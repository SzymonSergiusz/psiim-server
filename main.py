from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends

from db import models
from routes import mountains, production_only, users
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
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

app.include_router(production_only.router, tags=['Production tests'], prefix='/test')