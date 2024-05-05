from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import db.schemas as schemas
from auth.authorization import get_current_user
from db.database import get_db
import db.models as models

router = APIRouter()


# TODO czy dodawać to zabezpieczenie czterema cyframi?
@router.post('/{mountain_id}}', status_code=status.HTTP_201_CREATED)
async def user_unlocks_mountain(mountain_id: str, current_user: Annotated[schemas.User, Depends(get_current_user)],
                                           db: Session = Depends(get_db)):
    user_id = current_user.user_id
    to_add = models.Users_Mountains(user_id=user_id, mountain_id=mountain_id)
    db.add(to_add)
    db.commit()
    db.refresh(to_add)
