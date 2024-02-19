from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata


class Producer(ABC):
    """Абстрактный класс-интерфейс для брокера сообщений"""

    @abstractmethod
    async def send(self, *args, **kwargs):
        """Отравляет сообщение."""
        raise NotImplementedError


class KafkaProducer(Producer):

    async def send(
            self,
            producer: AIOKafkaProducer,
            topic: str,
            key: bytes,
            value: bytes
    ) -> RecordMetadata:
        result = await producer.send_and_wait(
            topic=topic, key=key, value=value
        )
        return result
