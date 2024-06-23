import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    repeat_password: str

class User(UserBase):
    user_id: UUID

    class Config:
        orm_mode = True

class AchievementBase(BaseModel):
    name: str | None = None
    description: str | None = None

class Achievement(AchievementBase):
    achievement_id: UUID

    class Config:
        orm_mode = True

class MountainBase(BaseModel):
    mountain_name: str | None = None
    description: str | None = None
    image_path: str | None = None
    image_source: str | None = None

class Mountain(MountainBase):
    mountain_id: UUID

    class Config:
        orm_mode = True
class MountainsList(BaseModel):
    mountains: List[MountainBase]
class CommentBase(BaseModel):
    content: str | None = None

class CommentCreate(CommentBase):
    user_id: UUID
    mountain_id: UUID
    root_comment_id: Optional[UUID] = None

class PrimaryCommentCreate(CommentBase):
    user_id: UUID | None = None
    mountain_id: UUID | None = None
class Comment(CommentBase):
    comment_id: UUID | None = None
    user: User | None = None
    mountain: Mountain | None = None
    replies: List["Comment"] = []

    class Config:
        orm_mode = True

class Users_AchievementsBase(BaseModel):
    user_id: UUID
    achievement_id: UUID

class Users_Achievements(Users_AchievementsBase):
    id: UUID

    class Config:
        orm_mode = True

class Users_MountainsBase(BaseModel):
    user_id: UUID
    mountain_id: UUID

class Users_Mountains(Users_MountainsBase):
    class Config:
        orm_mode = True
