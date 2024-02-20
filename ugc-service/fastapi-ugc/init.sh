#!/bin/bash
set -e

# Запускаем FastAPI-сервер
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b :$UGC_FASTAPI_PORT main:app
