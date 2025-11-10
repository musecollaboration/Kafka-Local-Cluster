import asyncio
import logging
from aiokafka import AIOKafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send():
    producer = AIOKafkaProducer(bootstrap_servers='kafka1:9092')
    await producer.start()
    try:
        value = b"hello world"
        await producer.send_and_wait("my-topic", value)
        logger.info("Сообщение отправлено: %r", value)
    except Exception as e:
        logger.error("Ошибка при отправке сообщения: %s", e)
    finally:
        await producer.stop()
        logger.info("Соединение с Kafka закрыто")

if __name__ == "__main__":
    asyncio.run(send())
