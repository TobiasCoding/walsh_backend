from pydantic import BaseModel
from typing import Dict
from datetime import datetime


# HAY QUE AJUSTART ESTO -------------- INICIO


class ConfigUpdate(BaseModel):
    service: str
    version: int
    payload: Dict[str, str]
    timestamp: datetime

    class Config:
        # Ese modelo solo documenta el formato del mensaje de configuración y permite validarlo si más adelante lo usás en endpoints o tests.
        # La sección json_schema_extra["example"] aparece en Swagger / OpenAPI para que quien consuma la API vea un ejemplo de payload válido; no tiene ningún efecto en tiempo de ejecución.
        json_schema_extra = {
            "example": {
                "service": "file_storage_service",
                "version": 1,
                "timestamp": "2025-05-30T23:45:00Z",
                "payload": {
                    "FILE_BASE_PATH": "/data/files",
                    "KAFKA_BOOTSTRAP": "kafka:9092",
                    "KAFKA_TOPIC": "file-storage-service",
                    "MAX_UPLOAD_MB": "100",
                },
            }
        }


# HAY QUE AJUSTART ESTO -------------- FIN
