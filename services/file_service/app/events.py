# app/events.py

from confluent_kafka import Producer
from datetime import datetime, timezone
from app.models import FileMeta, FileStoredEvent
from config.variables.file_storage import KAFKA_BOOTSTRAP, KAFKA_TOPIC
import json
import logging

logger = logging.getLogger(__name__)


def get_producer() -> Producer:
    return Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def publish_file_stored_event(key: str, meta: FileMeta):
    producer = get_producer()
    event = FileStoredEvent(key=key, meta=meta, timestamp=datetime.now(timezone.utc))
    json_payload = event.model_dump_json()
    try:
        producer.produce(
            topic=KAFKA_TOPIC, key=key.encode(), value=json_payload.encode()
        )
        producer.poll(0)
    except Exception as e:
        logger.exception(f"Error al publicar evento Kafka: {e}")


def test_kafka_connection():
    producer = get_producer()
    metadata = producer.list_topics(timeout=5)
    if KAFKA_TOPIC not in metadata.topics:
        raise RuntimeError(f"Tópico {KAFKA_TOPIC} no existe")
