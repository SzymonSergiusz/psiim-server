import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlite for production
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:bazydanych@localhost/psiim-db"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:bazydanych@localhost/psiim-db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
