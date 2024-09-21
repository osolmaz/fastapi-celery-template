# app.py
from fastapi import FastAPI, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Data
from tasks import process_data, celery_app
from celery.result import AsyncResult

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
def create_data(
    data_request: DataRequest, request: Request, db: Session = Depends(get_db)
):
    """Endpoint to create data and enqueue processing task."""
    data = Data(content=data_request.content)
    db.add(data)
    db.commit()
    db.refresh(data)
    # Enqueue the Celery task and get the task ID
    task = process_data.delay(data.id)
    task_id = task.id
    # Build the full URL to poll the task status
    task_url = request.url_for("get_task_status", task_id=task_id)
    return {"task_url": str(task_url)}


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """Endpoint to get the status and result of a task."""
    result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": result.status,
    }
    if result.status == "SUCCESS":
        # Retrieve the result from Celery's backend
        response["result"] = result.result
    elif result.status == "FAILURE":
        response["error"] = str(result.info)
    return response


@app.get("/data/{data_id}")
def get_data(data_id: int, db: Session = Depends(get_db)):
    """Endpoint to retrieve data."""
    data = db.query(Data).filter(Data.id == data_id).first()
    if data:
        return {"id": data.id, "content": data.content}
    else:
        raise HTTPException(status_code=404, detail="Data not found")
