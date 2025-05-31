# app/models.py

from pydantic import BaseModel
from typing import List
from datetime import datetime


class FileMeta(BaseModel):
    user_id: str
    tags: List[str]
    sha256: str
    created_at: datetime


class FileStoredEvent(BaseModel):
    key: str
    meta: FileMeta
    timestamp: datetime
