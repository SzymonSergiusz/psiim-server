import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, nullable=False)
    username = Column(String(256), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(512), nullable=False)

    achievements = relationship("Users_Achievements", back_populates="user")
    mountains = relationship("Users_Mountains", back_populates="user")
    comments = relationship("Comments", back_populates="user")

    def __repr__(self):
        return f"User(user_id='{self.user_id}', username='{self.username}', email='{self.email}')"


class Mountains(Base):
    __tablename__ = 'mountains'
    mountain_id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, nullable=False)
    mountain_name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String(256), nullable=False)
    image_source = Column(String(256), nullable=False)

    users = relationship("Users_Mountains", back_populates="mountain")
    comments = relationship("Comments", back_populates="mountain")

    def __repr__(self):
        return f"Mountain(mountain_id='{self.mountain_id}', mountain_name='{self.mountain_name}')"


class Achievements(Base):
    __tablename__ = 'achievements'
    achievement_id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, nullable=False)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)

    users = relationship("Users_Achievements", back_populates="achievement")

    def __repr__(self):
        return f'Achievement(id={self.achievement_id} name={self.name} desc = {self.description})'


class Comments(Base):
    __tablename__ = 'comments'

    comment_id = Column(GUID, primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(GUID, ForeignKey('users.user_id'), nullable=False)
    mountain_id = Column(GUID, ForeignKey('mountains.mountain_id'), nullable=False)
    root_comment_id = Column(GUID, ForeignKey('comments.comment_id'), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="comments")
    mountain = relationship("Mountains", back_populates="comments")
    replies = relationship("Comments", remote_side=[comment_id])

    def __repr__(self):
        return f"Comment(comment_id='{self.comment_id}', content='{self.content[:10]}')"


class Users_Achievements(Base):
    __tablename__ = 'users_achievements'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(GUID, ForeignKey('users.user_id'), nullable=False)
    achievement_id = Column(GUID, ForeignKey('achievements.achievement_id'), nullable=False)

    user = relationship("Users", back_populates="achievements")
    achievement = relationship("Achievements", back_populates="users")


class Users_Mountains(Base):
    __tablename__ = 'users_mountains'

    id = Column(GUID, primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(GUID, ForeignKey('users.user_id'), nullable=False)
    mountain_id = Column(GUID, ForeignKey('mountains.mountain_id'), nullable=False)

    user = relationship("Users", back_populates="mountains")
    mountain = relationship("Mountains", back_populates="users")
