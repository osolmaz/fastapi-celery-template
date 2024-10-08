# tasks.py
from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, DATABASE_URL, CONNECT_ARGS
from models import Data, Base
import time


celery_app = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Database configuration
engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task(bind=True)
def process_data(self, data_id):
    """Celery task to process data."""
    try:
        # Simulate a time-consuming task
        time.sleep(5)
        db = SessionLocal()
        data = db.query(Data).filter(Data.id == data_id).first()
        if data:
            # Example processing: convert content to uppercase
            processed_content = data.content.upper()
            data.content = processed_content
            db.commit()
            db.close()
            return {"processed_content": processed_content}
        else:
            db.close()
            self.update_state(state="FAILURE", meta={"exc": "Data not found"})
            raise Exception("Data not found")
    except Exception as e:
        self.update_state(state="FAILURE", meta={"exc": str(e)})
        raise
