from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from db import schemas, models
from db.database import get_db

router = APIRouter()


@router.post('/add')
async def add_to_users_collection(payload: schemas.Users_Mountains, db: Session = Depends(get_db)):
    item = models.Users_Mountains(user_id=payload.user_id, mountain_id=payload.mountain_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return status.HTTP_200_OK
