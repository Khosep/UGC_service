from aiokafka import AIOKafkaProducer

kafka_producer: AIOKafkaProducer | None = None


async def get_kafka_producer() -> AIOKafkaProducer:
    return kafka_producer
