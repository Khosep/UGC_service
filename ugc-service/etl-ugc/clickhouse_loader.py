from clickhouse_driver import Client

from core.config import settings
from core.logger import logger
from kafka_extractor import KafkaExtractor
from queries import INSERT_BUTCH, COUNT_ROWS


class ClickHouseLoader:
    """Класс для загрузки сообщений в ClickHouse."""

    def __init__(self):
        self.client = Client(host=settings.clickhouse_host)

    def load_batch(self, batch: list[dict], extractor: KafkaExtractor):
        """Загружает в ClickHouse партию записей."""

        self.client.execute(INSERT_BUTCH, batch)
        extractor.commit()
        logger.info(f"Добавлено {len(batch)} записей в ClickHouse")
        logger.info(f"Итого = {self.client.execute(COUNT_ROWS)[0][0]}")
