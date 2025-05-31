import json
from confluent_kafka import Producer
from datetime import datetime, timezone
import os

# VARIABLES DE KAFKA
# Se leen de entorno si están definidas, sino usamos valores por defecto:
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "configUpdate")

producer: Producer | None = None


def init_kafka_producer():
    """
    Inicializa un Producer global conectado al broker de Kafka.
    """
    global producer
    if producer is None:
        producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})


# En app/kafka_producer.py, reemplaza test_kafka_connection() por:
def test_kafka_connection():
    if producer is None:
        raise RuntimeError("Producer no inicializado")
    try:
        metadata = producer.list_topics(timeout=5.0)
    except Exception as e:
        print(f"[WARNING] No se pudo obtener metadata de Kafka: {e}")
        return
    # Si el tópico no existe, no intentamos crearlo aquí
    if KAFKA_TOPIC not in metadata.topics:
        print(
            f"[WARNING] Tópico '{KAFKA_TOPIC}' no encontrado, y no se crea automáticamente."
        )


def publish_config_update(service: str, version: int, payload: dict):
    """
    Publica un evento de configuración para 'service' en su topic privado.
    """
    if producer is None:
        raise RuntimeError("Producer de Kafka no inicializado")

    topic = f"config-{service.replace('_', '-')}"  # seguridad extra

    message = {
        "service": service,
        "version": version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }

    producer.produce(
        topic=topic,
        key=service.encode("utf-8"),
        value=json.dumps(message).encode("utf-8"),
    )
    producer.poll(0)
