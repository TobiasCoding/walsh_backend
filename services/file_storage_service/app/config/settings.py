# config/settings.py

from pydantic import BaseModel
from typing import Optional


class FileServiceSettings(BaseModel):
    FILE_BASE_PATH: str = "/data/files"
    FILE_PUBLIC_URL: str = "http://localhost:8004/files"
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_TOPIC: str = "file-storage-service"
    MAX_UPLOAD_MB: int = 50


# Instancia global
settings = FileServiceSettings()
