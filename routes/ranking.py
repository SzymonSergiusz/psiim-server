from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import db.schemas as schemas
from auth.authorization import get_current_user
from db.database import get_db
import db.models as models

router = APIRouter()


# @router.get('/')
# async def get_ranking(db: Session = Depends(get_db)):
#     pass

@router.get('/')
async def get_ranking(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    all_achievements = db.query(models.Achievements).all()
    

    ranking = []

    for user in users:
        user_achievements = db.query(models.Users_Achievements).filter(models.Users_Achievements.user_id == user.user_id).all()
        user_achievements_ids = {ua.achievement_id for ua in user_achievements}
        achieved = [ach for ach in all_achievements if ach.achievement_id in user_achievements_ids]
        achieved_count = len(achieved)
        ranking.append({'username': user.username, 'count': achieved_count})
        

    return {"ranking": ranking}