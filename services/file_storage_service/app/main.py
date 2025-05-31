# services/file_storage_service/app/main.py
# Microservicio: file_storage_service
# Ajustado a:
#   • Nuevo nombre de servicio (file_storage_service)
#   • Convención de topics “config-file-storage-service”
#   • Hilo consumidor de configuración dinámica

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from prometheus_client import make_asgi_app
from app.routes.files import router as files_router
from app.events import (
    test_kafka_connection,
)  # verifica tópico de “file-storage-service”
from app.config.config_consumer import consume_config  # loader Kafka → settings
from app.config.settings import settings
import os, threading
from app.common.logger import get_logger

logger = get_logger(__name__, service="file_storage_service")
logger.info("Servicio iniciado")

app = FastAPI(title="file_storage_service")

# --- Middleware CORS (abierto por defecto) ----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Middleware límite de tamaño -------------------------------------------
class UploadLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if (
            content_length
            and int(content_length) > settings.MAX_UPLOAD_MB * 1024 * 1024
        ):
            return JSONResponse(
                status_code=413,
                content={
                    "detail": f"Archivo supera el límite de {settings.MAX_UPLOAD_MB} MB"
                },
            )
        return await call_next(request)


app.add_middleware(UploadLimitMiddleware)

# --- Rutas API --------------------------------------------------------------
app.include_router(files_router, prefix="", tags=["files"])

# --- Métricas Prometheus ----------------------------------------------------
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# --- Startup: hilo consumidor de configuración -----------------------------
@app.on_event("startup")
def start_config_listener() -> None:
    """
    • Inicia thread que escucha “config-file-storage-service”
      y aplica cambios a `settings`.
    • Comprueba conexión a Kafka en salud (/healthz).
    """
    threading.Thread(target=consume_config, daemon=True).start()


# --- Health-check -----------------------------------------------------------
@app.get("/healthz")
async def healthz():
    # Verifica escritura en disco
    try:
        test_file = os.path.join(settings.FILE_BASE_PATH, ".healthcheck")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {e}")

    # Verifica conexión Kafka / tópico
    try:
        test_kafka_connection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {e}")

    return {"status": "ok"}
