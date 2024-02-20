from datetime import datetime

from pydantic import BaseModel


class KafkaMessage(BaseModel):
    key: bytes
    value: bytes


class FilmTimestampMessage(BaseModel):
    user_id: str
    film_id: str
    film_ts: int
    event_time: datetime
