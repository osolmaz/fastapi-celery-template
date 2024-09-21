# app.py
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Data
from tasks import process_data

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic model for request body
class DataRequest(BaseModel):
    content: str


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/data/")
def create_data(data_request: DataRequest, db: Session = Depends(get_db)):
    """Endpoint to create data and enqueue processing task."""
    data = Data(content=data_request.content)
    db.add(data)
    db.commit()
    db.refresh(data)
    # Enqueue the Celery task
    process_data.delay(data.id)
    return {"id": data.id, "content": data.content}


@app.get("/data/{data_id}")
def get_data(data_id: int, db: Session = Depends(get_db)):
    """Endpoint to retrieve data."""
    data = db.query(Data).filter(Data.id == data_id).first()
    if data:
        return {"id": data.id, "content": data.content}
    else:
        return {"error": "Data not found"}
