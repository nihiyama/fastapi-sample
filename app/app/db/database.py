from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.config import settings

engin = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    # connect_args={
    #     "check_same_thread": False},
    pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engin, autocommit=False, autoflush=False)

Base = declarative_base()
