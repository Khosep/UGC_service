from clickhouse_loader import ClickHouseLoader
from core.config import settings
from kafka_extractor import KafkaExtractor
from transformer import Transformer


def etl_process(
        extractor: KafkaExtractor,
        transformer: Transformer,
        loader: ClickHouseLoader
) -> None:
    batch = []
    for message in extractor.read():
        transformed_data = transformer.transform_film_timestamp(message)
        t = next(transformed_data)
        batch.append(t)
        if len(batch) >= settings.batch_size:
            loader.load_batch(batch, extractor)
            batch = []



if __name__ == '__main__':
    extractor = KafkaExtractor()
    transformer = Transformer()
    loader = ClickHouseLoader()

    etl_process(extractor, transformer, loader)
