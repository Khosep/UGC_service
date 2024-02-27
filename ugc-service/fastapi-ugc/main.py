import logging
import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Callable

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.middleware.base import _StreamingResponse
from starlette.middleware.sessions import SessionMiddleware

from api.v1 import stats
from core.config import settings
from core.logger import logger
from db import kafka


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Определение логики работы (запуска и остановки) приложения."""
    # Логика при запуске приложения.
    kafka.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}"
    )
    await kafka.kafka_producer.start()
    logger.info("App started")
    yield
    # Логика при завершении приложения.
    await kafka.kafka_producer.stop()
    logger.info("App stopped")
    # Добавим асинхронное закрытие обработчика файла
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    description=settings.description,
    version=settings.version,
    docs_url=settings.openapi_docs_url,
    openapi_url=settings.openapi_url,
    default_response_class=ORJSONResponse,
)

app.include_router(
    stats.router, prefix=settings.prefix + "/stats", tags=["Статистика"]
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(32),
    session_cookie=settings.session_cookie,
)

if settings.enable_tracer:

    @app.middleware("http")
    async def before_request(
        request: Request, call_next: Callable
    ) -> _StreamingResponse | ORJSONResponse:
        """Провереяет, имеется ли необходимый для трассировки заголовок."""

        if request.url.path.startswith(settings.prefix):
            request_id = request.headers.get("X-Request-Id")
            if not request_id:
                return ORJSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "X-Request-Id is required"},
                )

        response = await call_next(request)
        return response


async def http422_error_handler(request, exc: RequestValidationError):
    """Обработчик ошибок валидации Pydantic."""
    error_fields = [
        f'{error["loc"][1]}: {error["msg"]}' for error in exc.errors()
    ]
    error_msg = f"Ошибки по полям: {error_fields}."
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={"detail": error_msg},
    )


app.add_exception_handler(RequestValidationError, http422_error_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_fastapi_host,
        port=settings.ugc_fastapi_port,
    )
