from pydantic import BaseModel
from typing import Dict


class ConfigPayload(BaseModel):
    version: int
    payload: Dict[str, str]

    class Config:
        schema_extra = {
            "example": {
                "version": 2,
                "payload": {
                    "FILE_BASE_PATH": "/data/files",
                    "KAFKA_BOOTSTRAP": "kafka:9092",
                    "KAFKA_TOPIC": "file_stored",
                    "MAX_UPLOAD_MB": "100",
                },
            }
        }
