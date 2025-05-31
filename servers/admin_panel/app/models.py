from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class ConfigUpdate(BaseModel):
    service: str
    version: int
    payload: Dict[str, str]
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "service": "file_service",
                "version": 1,
                "timestamp": "2025-05-30T23:45:00Z",
                "payload": {
                    "FILE_BASE_PATH": "/data/files",
                    "KAFKA_BOOTSTRAP": "kafka:9092",
                    "KAFKA_TOPIC": "file_stored",
                    "MAX_UPLOAD_MB": "100",
                },
            }
        }
