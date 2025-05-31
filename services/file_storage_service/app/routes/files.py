# app/routes/files.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import StreamingResponse, Response
from hashlib import sha256
from datetime import datetime, timezone
from mimetypes import guess_type
import aiofiles, os
from app.models import FileMeta
from app.storage.local import LocalFSBackend
from app.events import publish_file_storage_event
from secrets import token_hex
from datetime import datetime
from secrets import token_hex
from app.config.settings import settings

router = APIRouter()
storage = LocalFSBackend(settings.FILE_BASE_PATH)


def generar_clave_archivo(
    origen: str, extension: str, base_path: str, max_reintentos: int = 10
) -> str:
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d")
    hora_min = datetime.now(timezone.utc).strftime("%H%M")
    for _ in range(max_reintentos):
        short_id = token_hex(3)  # 6 caracteres
        nombre_archivo = f"{hora_min}-{short_id}{extension}"
        clave = f"{origen}/{fecha}/{nombre_archivo}"
        ruta = os.path.join(base_path, clave)
        if not os.path.exists(ruta):
            return clave
    raise RuntimeError(
        f"No se pudo generar un nombre único después de {max_reintentos} intentos"
    )


@router.post("/files")
async def upload_file(request: Request, file: UploadFile = File(...)):
    user_id = request.headers.get("x-user-id", "anonymous")
    origen = request.headers.get("x-source", "unknown")  # microservicio llamante
    content = await file.read()

    extension = os.path.splitext(file.filename or "")[1].lower()

    try:
        key = generar_clave_archivo(origen, extension, settings.FILE_BASE_PATH)
        storage.save_file(key, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar archivo: {e}")

    hash_hex = sha256(content).hexdigest()
    meta = FileMeta(
        user_id=user_id, tags=[], sha256=hash_hex, created_at=datetime.utcnow()
    )
    publish_file_storage_event(key, meta)

    url = f"{settings.FILE_PUBLIC_URL}/{key}"
    return {"key": key, "url": url}


@router.get("/files/{key}")
async def get_file(key: str):
    try:
        path = os.path.join(settings.FILE_BASE_PATH, key)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        mime, _ = guess_type(path)
        mime = mime or "application/octet-stream"

        async def file_iterator():
            async with aiofiles.open(path, mode="rb") as f:
                while chunk := await f.read(8192):
                    yield chunk

        return StreamingResponse(file_iterator(), media_type=mime)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer archivo: {e}")


@router.head("/files/{key}")
async def head_file(key: str):
    path = os.path.join(settings.FILE_BASE_PATH, key)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    size = os.path.getsize(path)
    mime, _ = guess_type(path)
    mime = mime or "application/octet-stream"

    headers = {
        "Content-Length": str(size),
        "Content-Type": mime,
    }
    return Response(headers=headers)


@router.delete("/files/{key}")
async def delete_file(key: str):
    path = os.path.join(settings.FILE_BASE_PATH, key)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    try:
        os.remove(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo eliminar: {e}")
    return {"detail": "Archivo eliminado"}
