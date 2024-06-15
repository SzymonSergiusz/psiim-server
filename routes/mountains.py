from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import db.schemas as schemas
from auth.authorization import get_current_user
from db.database import get_db
import db.models as models

router = APIRouter()


@router.get('/')
async def get_all_mountains(db: Session = Depends(get_db)):
    return {'mountains': db.query(models.Mountains).all()}


@router.get('/id/{mountain_id}')
async def get_mountain(mountain_id: str, db: Session = Depends(get_db)):
    query = db.query(models.Mountains).filter(models.Mountains.mountain_id == mountain_id)
    mountain = query.first()
    if not mountain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Mountain not found')

    return {mountain}


@router.get('/count', status_code=status.HTTP_200_OK)
async def count_mountains(db: Session = Depends(get_db)):
    return {'count': db.query(models.Mountains).count()}


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_mountain(payload: schemas.Mountain, db: Session = Depends(get_db)):
    new_mountain = models.Mountains(**payload.dict())
    db.add(new_mountain)
    db.commit()
    db.refresh(new_mountain)

    return {"status": "success", "mountain": new_mountain}


@router.post('/from_array', status_code=status.HTTP_201_CREATED)
async def add_mountains(payload: schemas.MountainsList, db: Session = Depends(get_db)):
    new_mountains = [models.Mountains(**mountain.dict()) for mountain in payload.mountains]
    db.add_all(new_mountains)
    db.commit()
    for mountain in new_mountains:
        db.refresh(mountain)

    return {"status": "success", "mountains": new_mountains}

@router.patch('/id/{mountain_id}')
async def update_mountain(mountain_id: str, payload: schemas.Mountain, db: Session = Depends(get_db)):
    query = db.query(models.Mountains).filter(models.Mountains.mountain_id == mountain_id)
    mountain = query.first()
    if not mountain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Mountain not found')
    update_row = payload.dict(exclude_unset=True)
    query.filter(models.Mountains.mountain_id == mountain_id).update(update_row, synchronize_session=False)
    db.commit()
    db.refresh(mountain)
    return {mountain}

@router.get('/users_mountains', status_code=status.HTTP_200_OK)
async def get_all_logged_user_achievements(current_user: Annotated[schemas.User, Depends(get_current_user)],
                                           db: Session = Depends(get_db)):
    
    user_id = current_user.user_id

    user_mountains = db.query(models.Users_Mountains).filter(models.Users_Mountains.user_id == user_id).all()
    user_mountains_ids = {ua.mountain_id for ua in user_mountains}

    all_mountains = db.query(models.Mountains).all()

    achieved = [ach for ach in all_mountains if ach.mountain_id in user_mountains_ids]
    not_achieved = [ach for ach in all_mountains if ach.mountain_id not in user_mountains_ids]

    achieved_count = len(achieved)
    not_achieved_count = len(not_achieved)

    return {
        "achieved": achieved,
        "not_achieved": not_achieved,
        "achieved_count": achieved_count,
        "not_achieved_count": not_achieved_count
    }

    # return db.query(models.Users_Mountains).filter(models.Users_Mountains.user_id == user.user_id).all()

    # testowo
    # powinno zwrócić zdobyte góry oraz ile jest zdobytych a ile niezdobytych (do tych liczników
    # format: {unlocked: //zdobyte, locked: //niezdobyte, count_unlock, count_unlock}
