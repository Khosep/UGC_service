#!/bin/bash
set -e

# Ждем, пока база данных станет доступной
until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Выполняем миграции
poetry run alembic upgrade head

# Запускаем FastAPI-сервер
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b :$UGC_FASTAPI_PORT main:app
