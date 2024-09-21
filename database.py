# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL, CONNECT_ARGS


engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
