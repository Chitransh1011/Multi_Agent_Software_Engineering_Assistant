#!/bin/sh

echo "Waiting for PostgreSQL..."

until pg_isready -h db -U postgres
do
    sleep 2
done

echo "PostgreSQL is ready."

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000