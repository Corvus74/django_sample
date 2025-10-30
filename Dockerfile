# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install build dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Set work directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Configure poetry to create the venv in the project directory
RUN poetry config virtualenvs.in-project true

# Copy poetry files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

# Copy project
COPY . /app/

# Expose port 8000
EXPOSE 8000

# For production, use Gunicorn with a Uvicorn worker for ASGI applications.
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "DjangoSample.asgi:application", "--bind", "0.0.0.0:8000"]
