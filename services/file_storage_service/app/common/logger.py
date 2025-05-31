# common/logger.py
import logging, sys, json, os
from typing import Optional, Union


class JSONFormatter(logging.Formatter):
    """
    Formato JSON amigable para stack ELK / Loki-Grafana.
    El nombre del servicio se toma en este orden:
      1. Atributo extra del log (“service”)
      2. Variable de entorno SERVICE_NAME
      3. Prefijo del logger (p. ej. “file_storage_service” en
         get_logger("file_storage_service.main"))
    """

    def format(self, record: logging.LogRecord) -> str:
        service = (
            getattr(record, "service", None)
            or os.getenv("SERVICE_NAME")
            or record.name.split(".", 1)[0]
        )

        log = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": service,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log)


def get_logger(
    name: str = "app",
    level: int = logging.INFO,
    service: Optional[str] = None,
) -> Union[logging.Logger, logging.LoggerAdapter]:
    """
    Devuelve un logger con salida JSON a stdout.

    • Si pasás `service`, se añade como extra a todos los registros.
    • Si querés algo más simple, seteá SERVICE_NAME en el contenedor
      y llamá `get_logger(__name__)`.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # evita duplicar handlers

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False

    if service:
        return logging.LoggerAdapter(logger, {"service": service})
    return logger
