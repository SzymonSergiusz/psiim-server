from fastapi import APIRouter, status, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import db.schemas as schemas
import db.models as models
from db.database import get_db

router = APIRouter()


@router.get('/')
async def get_users(db: Session = Depends(get_db)):
    return {'users': db.query(models.Users).all()}
