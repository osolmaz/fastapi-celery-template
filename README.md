# FastAPI + Celery + SQLAlchemy Boilerplate

This project is a simple boilerplate for building a web application using FastAPI, Celery, and SQLAlchemy. It demonstrates how to set up a project with these technologies, including task enqueuing and processing.

SQLAlchemy is used as the result backend and broker.

## Installation

Package manager `uv` needs to be installed.

```
uv sync
```

## Usage

Start the FastAPI server and Celery worker:

```
uv run uvicorn app:app --reload
uv run celery -A tasks.celery_app worker --loglevel=info
```

Run the client to create a task:

```
python client.py
```
