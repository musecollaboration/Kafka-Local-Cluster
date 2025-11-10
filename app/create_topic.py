
import os
import asyncio
import logging
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka1:9092,kafka2:9092,kafka3:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "my-topic")
REPLICATION_FACTOR = int(os.getenv("KAFKA_REPLICATION", "3"))
PARTITIONS = int(os.getenv("KAFKA_PARTITIONS", "1"))


async def create_topic():
    admin = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        await admin.start()
        logger.info(f"Connected to Kafka cluster at {KAFKA_BOOTSTRAP_SERVERS}")
        topic = NewTopic(
            name=TOPIC_NAME,
            num_partitions=PARTITIONS,
            replication_factor=REPLICATION_FACTOR
        )
        await admin.create_topics([topic])
        logger.info(f"Topic '{TOPIC_NAME}' created successfully")
    except TopicAlreadyExistsError:
        logger.info(f"Topic '{TOPIC_NAME}' already exists")
    except Exception as e:
        logger.error(f"Error creating topic: {e}")
        raise
    finally:
        await admin.close()
        logger.info("Kafka admin connection closed")

if __name__ == "__main__":
    asyncio.run(create_topic())
