import os
import json
import logging

from kafka import KafkaProducer
from kafka_helpers import publish
from lemmy_helpers import fetch_posts

from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def create_kafka_producer(bootstrap_servers: list) -> KafkaProducer:
    logger.info("Creating Kafka producer...")
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


def main():
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    lemmy_node = os.environ["LEMMY_NODE"]
    community_name = os.environ["COMMUNITY"]
    start_page = int(os.environ.get("START_PAGE", 1))
    limit = int(os.environ.get("LIMIT", 50))


    topic = os.environ["KAFKA_TOPIC"]
    bootstrap_servers = os.environ.get("KAFKA_BROKER").split(",")
    producer = create_kafka_producer(bootstrap_servers)

    posts = fetch_posts(
        username, password,
        lemmy_node, community_name,
        page=start_page,
        limit=limit,
    )

    for post in posts:
        logger.info(f"Publishing post id={post['id']} title={post['title']!r}")
        publish(topic, post, producer)
        comments = {
            "id": post["id"],
            "comments": "This looks interesting! Can't wait to read more."
        }
        logger.info(f"Publishing comment for post id={post['id']}")
        publish(topic, comments, producer)

    producer.flush()

    logger.info("Closing Kafka producer...")
    producer.close()

    logger.info("Done.")


if __name__ == "__main__":
    main()
