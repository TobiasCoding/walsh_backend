# services/file_storage_service/app/events.py
from confluent_kafka import Producer, KafkaException
from app.common.logger import get_logger
from datetime import datetime, timezone
from app.models import FileMeta, FileStoredEvent
from app.common.config_store import settings

logger = get_logger(__name__, service="file_storage_service")


def get_producer() -> Producer:
    return Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP})


def publish_file_storage_event(key: str, meta: FileMeta):
    producer = get_producer()
    event = FileStoredEvent(key=key, meta=meta, timestamp=datetime.now(timezone.utc))
    json_payload = event.model_dump_json()
    try:
        producer.produce(
            topic=settings.KAFKA_TOPIC, key=key.encode(), value=json_payload.encode()
        )
        producer.poll(0)
    except Exception as e:
        logger.exception(f"Error al publicar evento Kafka: {e}")


def test_kafka_connection(kafka_topic: str) -> None:
    """
    Intenta enviar un mensaje vacío al topic indicado para verificar que existe.
    Lanza excepción si falla.
    """
    p = Producer({"bootstrap.servers": settings.KAFKA_BOOTSTRAP})
    try:
        p.produce(kafka_topic, key="healthcheck", value="")
        p.flush(timeout=5)
        logger.info(f"Kafka OK: puede publicar en {kafka_topic}")
    except KafkaException as e:
        logger.error(f"Error al conectar con Kafka/topic {kafka_topic}: {e}")
        raise
