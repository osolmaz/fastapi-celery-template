# tasks.py
from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, DATABASE_URL
from models import Data, Base
import time


celery_app = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Database configuration
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task
def process_data(data_id):
    """Celery task to process data."""
    # Simulate a time-consuming task
    time.sleep(5)
    db = SessionLocal()
    data = db.query(Data).filter(Data.id == data_id).first()
    if data:
        # Example processing: convert content to uppercase
        data.content = data.content.upper()
        db.commit()
    db.close()
