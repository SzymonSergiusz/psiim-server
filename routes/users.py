from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, status, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import db.schemas as schemas
import db.models as models
from auth.authorization import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from db.database import get_db
# from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(get_current_user)]):
    return {"token": token}


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:

        if user.password != user.repeat_password:
            return {"status": "incorrect repeat password"}

        hashed_password = pwd_context.hash(user.password)
        query_user = models.Users(email=user.email,
                                  password=hashed_password, username=user.username)
        db.add(query_user)
        db.commit()
        db.refresh(query_user)
        return {"status": "success"}
    except:
        return {"status": "failure"}


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)):
    query = db.query(models.Users).filter(models.Users.email == form_data.username)
    user = query.first()

    if not user and not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer", user_id= str(user.user_id))


@router.get('/users_count')
async def get_user_count(db: Session = Depends(get_db)):
    return {'users_count: ': db.query(models.Users).count()}
