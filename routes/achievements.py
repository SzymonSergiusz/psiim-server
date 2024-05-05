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
    # TODO do dokończenia
    user: models.Users = current_user

    # niedokonczone query, tutaj powinno być select z Mountains które się pokrywają z usersachievs gdzie userid jest takie samo
    db.query(models.Users_Achievements).filter(models.Users_Achievements.user_id == user.user_id).all()

    # testowo
    # powinno zwrócić zdobyte osiągnięcia, niezdobyte, oraz ile jest zdobytych a ile niezdobytych (do tych liczników
    # format: {unlocked: //zdobyte, locked: //niezdobyte, count_unlock, count_unlock}
    return {user.email}

@router.get('/all', status_code=status.HTTP_200_OK)
async def get_all_achievements(db: Session = Depends(get_db)):
    return {'achievements': db.query(models.Achievements).all()}

@router.post('add_achievement', status_code=status.HTTP_201_CREATED)
async def add_achievement(payload: schemas.Achievement, db: Session = Depends(get_db)):
    new_achievement = models.Achievements(**payload.dict())
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)

