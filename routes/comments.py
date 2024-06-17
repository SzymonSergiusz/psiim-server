from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import schemas, models
from db.database import get_db

router = APIRouter()


@router.post('/add')
async def add_comment(payload: schemas.PrimaryCommentCreate, db: Session = Depends(get_db)):
    item = models.Comments(
        user_id=str(payload.user_id),
        mountain_id=str(payload.mountain_id),
        content=payload.content,
        created_at=func.now()
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return status.HTTP_200_OK
@router.post('/answer')
async def add_comment(payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    item = models.Comments(
        user_id=str(payload.user_id),
        mountain_id=str(payload.mountain_id),
        content=payload.content,
        root_comment_id=payload.root_comment_id,
        created_at=func.now()
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return status.HTTP_200_OK
