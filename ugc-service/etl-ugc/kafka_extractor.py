from abc import ABC, abstractmethod
from typing import Generator

from kafka import KafkaConsumer

from core.config import settings
from core.logger import logger
from models import KafkaMessage


class Extractor(ABC):
    """Абстрактный класс-интерфейс для чтения из брокера сообщений."""

    @abstractmethod
    async def read(self, *args, **kwargs):
        """Чтение сообщения из брокера."""
        raise NotImplementedError

    @abstractmethod
    async def commit(self, *args, **kwargs):
        """Подтверждение, что прочитано"""
        raise NotImplementedError


class KafkaExtractor(Extractor):
    """Класс для чтения сообщений из Kafka."""
    def __init__(self):
        self.consumer = KafkaConsumer(
            settings.kafka_topic_timestamp,
            bootstrap_servers=[f"{settings.kafka_host}:{settings.kafka_port}"],
            group_id="film_stats",
            enable_auto_commit=False,
            auto_offset_reset='earliest'
        )

    def read(self) -> Generator[KafkaMessage, None, None]:
        """Читаем сообщение из Kafka."""

        for message in self.consumer:
            logger.debug(f"Прочитано сообщение ({message})")
            yield KafkaMessage(key=message.key, value=message.value)

    def commit(self):
        """
        Посылаем сигнал, что сообщения прочитаны
        (для подтверждения смещения (offset) в топике Kafka).
        """
        self.consumer.commit()
