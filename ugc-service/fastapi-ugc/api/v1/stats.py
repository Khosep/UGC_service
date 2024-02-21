from http import HTTPStatus
from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, Header

from core.config import settings
from db.kafka import get_kafka_producer
from schemas.stats_schema import FilmTimestamp
from services.stats_service import StatsService, get_stats_service
from services.token_service import get_token_service, TokenService

router = APIRouter()


@router.post(
    "/",
    status_code=HTTPStatus.OK,
    description="Отправить временную метку по фильму.",
)
async def send_film_timestamp(
    token_service: Annotated[TokenService, Depends(get_token_service)],
    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
    film_data: FilmTimestamp,
    stats_service: Annotated[StatsService, Depends(get_stats_service)],
    authorization: str = Header(None),
) -> dict[str, str]:
    """
    Отправляет для анализа метку просмотра фильма (секунды) пользователем
     в брокер сообщений.
    """
    token = token_service.extract_token(authorization)
    token_data = None
    if token:
        token_data = token_service.get_token_data(token)
    result = await stats_service.send_film_timestamp_to_broker(
        producer=producer,
        topic=settings.kafka_topic_timestamp,
        token_data=token_data,
        film_data=film_data,
    )
    return {"status": f"success {result}"}
