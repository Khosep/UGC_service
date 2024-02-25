import ast

from datetime import datetime
from typing import Generator

from models import KafkaMessage, FilmTimestampMessage


class Transformer:
    """
    Класс для трансформации сообщений из Kafka в формат,
    позволяющий вставить данные в ClickHouse.
    """

    def transform_film_timestamp(
            self, message: KafkaMessage
    ) -> Generator:
        """Преобразуем данные для временной метки по фильму."""

        dict_message = ast.literal_eval(message.value.decode("utf-8").replace("UUID", ""))
        data = FilmTimestampMessage(
            **dict_message,
            event_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        yield data.model_dump()
