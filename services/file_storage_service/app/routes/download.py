# services/file_storage_service/app/routes/download.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response
from mimetypes import guess_type
import aiofiles
import os
from app.common.config_store import settings

router = APIRouter()


def _find_file_by_name(base_path: str, filename: str) -> str | None:
    """
    Busca recursivamente dentro de base_path un archivo cuyo nombre sea 'filename'.
    Devuelve la ruta absoluta completa si lo encuentra, o None si no existe.
    """
    for root, _, files in os.walk(base_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Descarga un archivo a partir de su nombre único (p. ej. "0056-abc123.pdf"),
    sin exponer fecha/origen en la URL.
    """
    if not hasattr(settings, "FILE_BASE_PATH"):
        raise HTTPException(status_code=503, detail="Configuración pendiente")

    # Buscar el archivo en todo el árbol bajo FILE_BASE_PATH
    full_path = _find_file_by_name(settings.FILE_BASE_PATH, filename)
    if full_path is None or not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    mime, _ = guess_type(full_path)
    mime = mime or "application/octet-stream"

    async def file_iterator():
        async with aiofiles.open(full_path, mode="rb") as f:
            while chunk := await f.read(8192):
                yield chunk

    return StreamingResponse(
        file_iterator(),
        media_type=mime,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.head("/download/{filename}")
async def download_head(filename: str):
    """
    Devuelve solo metadatos (Content-Length, Content-Type) para un archivo dado su nombre.
    """
    if not hasattr(settings, "FILE_BASE_PATH"):
        raise HTTPException(status_code=503, detail="Configuración pendiente")

    full_path = _find_file_by_name(settings.FILE_BASE_PATH, filename)
    if full_path is None or not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    size = os.path.getsize(full_path)
    mime, _ = guess_type(full_path)
    mime = mime or "application/octet-stream"

    headers = {
        "Content-Length": str(size),
        "Content-Type": mime,
    }
    return Response(headers=headers)
