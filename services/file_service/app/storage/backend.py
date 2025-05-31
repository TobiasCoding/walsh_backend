# app/storage/backend.py

from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """Interfaz abstracta para backends de almacenamiento."""

    @abstractmethod
    def save_file(self, key: str, data: bytes) -> None:
        """Guarda un archivo binario bajo una clave única."""
        pass

    @abstractmethod
    def get_file(self, key: str) -> bytes:
        """Recupera un archivo binario por clave."""
        pass

    @abstractmethod
    def delete_file(self, key: str) -> None:
        """Elimina un archivo almacenado (lógico o físico)."""
        pass

    @abstractmethod
    def file_exists(self, key: str) -> bool:
        """Verifica si un archivo existe."""
        pass
