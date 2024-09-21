# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install uv
# RUN poetry config virtualenvs.create false
# RUN poetry install --no-dev

# Copy project
# COPY . .
COPY *.py .
COPY README.md .
COPY pyproject.toml ./
COPY uv.lock ./

RUN uv pip install . --system

# Expose port for FastAPI
EXPOSE 8000


# Entry point
# CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
