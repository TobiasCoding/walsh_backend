# app/storage/local.py

import os
from pathlib import Path
from app.storage.backend import StorageBackend


class LocalFSBackend(StorageBackend):
    """Implementación del backend que guarda archivos en el sistema de archivos local."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, key: str) -> Path:
        return self.base_path / key

    def save_file(self, key: str, data: bytes) -> None:
        path = self._resolve_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def get_file(self, key: str) -> bytes:
        path = self._resolve_path(key)
        if not path.exists():
            raise FileNotFoundError(f"Archivo {key} no encontrado")
        return path.read_bytes()

    def delete_file(self, key: str) -> None:
        path = self._resolve_path(key)
        if path.exists():
            path.unlink()

    def file_exists(self, key: str) -> bool:
        return self._resolve_path(key).exists()
