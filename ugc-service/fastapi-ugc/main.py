import logging
import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Callable

import uvicorn
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, ORJSONResponse
from redis.asyncio import Redis
from starlette.middleware.base import _StreamingResponse
from starlette.middleware.sessions import SessionMiddleware

from api.v1 import like
from core.config import settings
from core.logger import logger
from core.rate_limit import apply_rate_limit
from db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Определение логики работы (запуска и остановки) приложения."""
    # Логика при запуске приложения.
    redis.redis = Redis(
        host=settings.ugc_redis_host,
        port=settings.ugc_redis_port,
        db=0,
        decode_responses=True,
    )
    logger.info("Приложение запущено")
    logger.info(f"Redis ping: {await redis.redis.ping()}")
    yield
    # Логика при завершении приложения.
    await redis.redis.close()
    logger.info("Приложение остановлено")
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
    dependencies=[Depends(apply_rate_limit)],
)

app.include_router(
    like.router, prefix=settings.prefix + "/like", tags=["Лайки"]
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(32),
    session_cookie=settings.session_cookie,
)


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
