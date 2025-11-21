import os
import json
import logging

from dotenv import load_dotenv
from kafka import KafkaConsumer


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


    
def main():
    community_name = os.environ["COMMUNITY"]
    bootstrap_servers = os.environ["KAFKA_BROKER"].split(",")
    topic = os.environ["KAFKA_TOPIC"]

    logger.info("Creating Kafka consumer...")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        group_id=f"{community_name}-consumer-group",
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    try:
        for message in consumer:
            if "comments" in message.value:
                logger.info(f"Consumed message: {message.value}")
    except Exception as e:
        logger.error(f"An exception has occurred: {e}")
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
