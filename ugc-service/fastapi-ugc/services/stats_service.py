from functools import lru_cache
from typing import Type
from uuid import UUID

from aiokafka import AIOKafkaProducer

from schemas.stats_schema import FilmTimestamp
from services.broker_service import Producer, KafkaProducer


class StatsService:

    def __init__(self, producer_service: Type[Producer]):
        self.producer_service = producer_service()

    async def send_film_timestamp_to_broker(
            self,
            producer: AIOKafkaProducer,
            topic: str,
            user_id: UUID,
            film_data: FilmTimestamp
    ):
        key = self._str_to_bytes(f"{str(user_id)}_{str(film_data.film_id)}")
        value = self._str_to_bytes(str(film_data.film_timestamp_sec))
        result = await self.producer_service.send(
            producer=producer,
            topic=topic,
            key=key,
            value=value
        )
        return result

    def _str_to_bytes(self, string: str) -> bytes:
        encoded_string = string.encode("utf-8")
        return encoded_string


@lru_cache()
def get_stats_service() -> StatsService:
    return StatsService(KafkaProducer)
