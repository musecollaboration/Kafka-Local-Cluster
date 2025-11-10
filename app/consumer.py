import asyncio
import logging
from aiokafka import AIOKafkaConsumer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume():
    consumer = AIOKafkaConsumer(
        "my-topic",
        bootstrap_servers='kafka1:9092',
        group_id="test-group"
    )
    await consumer.start()
    logger.info("Консьюмер запущен и слушает топик 'my-topic'")
    try:
        async for msg in consumer:
            logger.info("Получено сообщение: %r", msg.value)
    except Exception as e:
        logger.error("Ошибка при получении сообщения: %s", e)
    finally:
        await consumer.stop()
        logger.info("Соединение с Kafka закрыто")

if __name__ == "__main__":
    asyncio.run(consume())
