# services/file_storage_service/app/main.py

# MODULOS EXTERNOS
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from prometheus_client import make_asgi_app

# ROUTERS
from app.routes.save import router as save_router
from app.routes.download import router as download_router

# OTROS PROPIOS
from app.events import test_kafka_connection
from app.common.config_store import settings
from app.common.config_loader import start_config_listener
from app.common.logger import get_logger
import os

logger = get_logger(__name__, service="file_storage_service")
logger.info("Servicio iniciado – esperando configuración por Kafka")

app = FastAPI(title="file_storage_service")

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware límite de tamaño dinámico ---
class UploadLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Verificamos que exista MAX_UPLOAD_MB en settings
        if not hasattr(settings, "MAX_UPLOAD_MB"):
            return JSONResponse(
                status_code=503,
                content={"detail": "Configuración pendiente desde admin_panel"},
            )

        # Forzamos a int en caso de que _cast no lo hiciera
        try:
            max_mb = int(settings.MAX_UPLOAD_MB)
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"detail": "MAX_UPLOAD_MB inválido"}
            )

        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_mb * 1024 * 1024:
            return JSONResponse(
                status_code=413,
                content={"detail": f"Máximo {max_mb} MB"},
            )

        return await call_next(request)

app.add_middleware(UploadLimitMiddleware)

@app.middleware("http")
async def ensure_config(request: Request, call_next):
    # Verificamos que lleguen todas las claves necesarias antes de atender cualquier ruta
    REQUIRED = ["FILE_BASE_PATH", "MAX_UPLOAD_MB", "KAFKA_TOPIC"]
    faltantes = [k for k in REQUIRED if not hasattr(settings, k)]
    if faltantes:
        raise HTTPException(
            status_code=503, detail=f"Configuración pendiente: faltan {faltantes}"
        )
    return await call_next(request)

# --- Rutas API ---
app.include_router(save_router, prefix="", tags=["files"])
app.include_router(download_router, prefix="", tags=["download"])

# --- Métricas Prometheus ---
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# --- Startup: hilo consumidor de configuración ---
@app.on_event("startup")
def start_config_listener_event() -> None:
    kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    start_config_listener(settings, "file_storage_service", kafka_bootstrap)

# --- Health-check ---
@app.get("/healthz")
async def healthz():
    required = ["FILE_BASE_PATH", "KAFKA_TOPIC", "MAX_UPLOAD_MB"]
    missing = [k for k in required if not hasattr(settings, k)]
    if missing:
        raise HTTPException(
            status_code=503, detail=f"Faltan variables de configuración: {missing}"
        )

    # Verifico escritura en disco
    try:
        test_file = os.path.join(settings.FILE_BASE_PATH, ".healthcheck")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {e}")

    # Verifico topic de Kafka (pasa el nombre desde settings)
    try:
        test_kafka_connection(settings.KAFKA_TOPIC)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {e}")

    return {"status": "ok"}
