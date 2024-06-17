from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import db.schemas as schemas
import db.models as models
from db.database import get_db
from auth.authorization import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/users_achievements', status_code=status.HTTP_200_OK)
async def get_all_logged_user_achievements(current_user: Annotated[schemas.User, Depends(get_current_user)],
                                           db: Session = Depends(get_db)):
    
    user_id = current_user.user_id

    user_achievements = db.query(models.Users_Achievements).filter(models.Users_Achievements.user_id == user_id).all()
    user_achievements_ids = {ua.achievement_id for ua in user_achievements}

    all_achievements = db.query(models.Achievements).all()

    achieved = [ach for ach in all_achievements if ach.achievement_id in user_achievements_ids]
    not_achieved = [ach for ach in all_achievements if ach.achievement_id not in user_achievements_ids]

    achieved_count = len(achieved)
    not_achieved_count = len(not_achieved)

    return {
        "achieved": achieved,
        "not_achieved": not_achieved,
        "achieved_count": achieved_count,
        "not_achieved_count": not_achieved_count
    }

@router.get('/all', status_code=status.HTTP_200_OK)
async def get_all_achievements(db: Session = Depends(get_db)):
    return {'achievements': db.query(models.Achievements).all()}

@router.post('/add_achievement', status_code=status.HTTP_201_CREATED)
async def add_achievement(payload: schemas.Achievement, db: Session = Depends(get_db)):
    new_achievement = models.Achievements(**payload.dict())
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)

