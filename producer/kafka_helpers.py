import uuid
import logging

from dataclasses import dataclass
from functools import wraps
from kafka import KafkaProducer


logger = logging.getLogger(__name__)


@dataclass
class FlushAfter:
    flush_after_count: int = 10

    _current_queue_size: int = 0

    def __call__(self, publish_fn):
        @wraps(publish_fn)
        def wrapper(topic: str, post: dict, producer: KafkaProducer):
            result = publish_fn(topic, post, producer)
            self._current_queue_size += 1
            if self._current_queue_size % self.flush_after_count == 0:
                logger.info("Flushing Kafka producer...")
                producer.flush()
                self._current_queue_size = 0            
            return result
        return wrapper


flush_after = FlushAfter()


@flush_after
def publish(topic: str, post: dict, producer: KafkaProducer) -> None:
    producer.send(topic, key=uuid.uuid4().bytes, value=post)
