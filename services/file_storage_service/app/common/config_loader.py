# services/file_storage_service/app/common/config_loader.py
import json, threading
from confluent_kafka import Consumer
from typing import Any
from app.common.logger import get_logger

logger = get_logger(__name__, service="file_storage_service")

def _cast(value: Any, current: Any):
    """
    Si 'current' ya existía, intenta type(current)(value).
    Si current es None, aplica json.loads(value) para inferir tipo.
    Si todo falla, retorna value tal cual.
    """
    # Si ya teníamos un valor, lo casteamos al mismo tipo
    if current is not None:
        try:
            return type(current)(value)
        except Exception:
            return value

    # Si current es None, intentamos inferir tipo via JSON
    try:
        return json.loads(value)
    except Exception:
        return value


class ConfigLoader:
    """
    Escucha mensajes en "config-<service>" y crea/actualiza atributos
    en el objeto 'settings'. 
    """

    def __init__(self, settings_obj, service_name: str, bootstrap: str):
        self.settings = settings_obj
        self.service = service_name
        self.topic = f"config-{service_name.replace('_', '-')}"
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap,
            "group.id": f"{service_name}_config_loader",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        })
        self.consumer.subscribe([self.topic])
        logger.info(f"Escuchando {self.topic}…")

    def _apply(self, payload: dict):
        for k, v in payload.items():
            current = getattr(self.settings, k, None)
            new_val = _cast(v, current)
            setattr(self.settings, k, new_val)
            logger.info(f"{k}={new_val}")  # mensaje más limpio

    def run(self):
        while True:
            msg = self.consumer.poll(1.0)
            if not msg:
                continue
            if msg.error():
                logger.warning(msg.error())
                continue
            try:
                data = json.loads(msg.value())
                if data.get("service") == self.service and "payload" in data:
                    self._apply(data["payload"])
            except Exception as e:
                logger.exception(f"Error procesando config: {e}")


def start_config_listener(settings_obj, service_name: str, kafka_bootstrap: str):
    """
    Lanza un hilo daemon con el consumer que escucha
    `config-<service_name>` y actualiza `settings_obj`.
    """
    loader = ConfigLoader(settings_obj, service_name, kafka_bootstrap)
    threading.Thread(target=loader.run, daemon=True).start()
