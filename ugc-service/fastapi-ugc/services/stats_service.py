from functools import lru_cache
from typing import Type

from aiokafka import AIOKafkaProducer

from schemas.stats_schema import FilmTimestamp
from schemas.token_schema import Token
from services.broker_service import Producer, KafkaProducer


class StatsService:
    def __init__(self, producer_service: Type[Producer]):
        self.producer_service = producer_service()

    async def send_film_timestamp_to_broker(
        self,
        producer: AIOKafkaProducer,
        topic: str,
        film_data: FilmTimestamp,
        token_data: Token | None = None,
    ):
        user_id = "anonimous"
        data = film_data.model_dump()
        if token_data:
            data.update(token_data.model_dump())
            user_id = token_data.user_id
        key = self._str_to_bytes(f"{str(user_id)}_{str(film_data.film_id)}")
        value = self._str_to_bytes(str(data))
        result = await self.producer_service.send(
            producer=producer, topic=topic, key=key, value=value
        )
        return result

    def _str_to_bytes(self, string: str) -> bytes:
        encoded_string = string.encode("utf-8")
        return encoded_string


@lru_cache()
def get_stats_service() -> StatsService:
    return StatsService(KafkaProducer)
