# config/config_consumer.py

import json
import threading
from confluent_kafka import Consumer, KafkaException
from config.settings import settings

TOPIC = "config-file-storage-service"
GROUP_ID = "file_storage_service_config_loader"


def apply_config(payload: dict):
    for k, v in payload.items():
        if hasattr(settings, k):
            casted = type(getattr(settings, k))(v)
            setattr(settings, k, casted)
            print(f"[CONFIG] {k} = {casted}")


def consume_config():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP,
            "group.id": GROUP_ID,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
    )
    consumer.subscribe([TOPIC])

    print(f"[CONFIG] Escuchando configuración en {TOPIC}...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"[CONFIG] Error: {msg.error()}")
            continue
        try:
            data = json.loads(msg.value().decode("utf-8"))
            if data.get("service") == "file_storage_service":
                apply_config(data["payload"])
        except Exception as e:
            print(f"[CONFIG] Error procesando mensaje: {e}")
