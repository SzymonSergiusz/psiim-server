from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import db.schemas as schemas
from auth.authorization import get_current_user
from db.database import get_db
import db.models as models

router = APIRouter()


@router.get('/')
async def get_ranking(db: Session = Depends(get_db)):
    pass