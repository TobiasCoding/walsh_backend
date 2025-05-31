# app/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.routes.files import router as files_router
from app.events import test_kafka_connection
import os
from config.variables.security import ALLOWED_EXTENSIONS


settings = get_settings()
app = FastAPI(title="file_service")

# Middleware: CORS (si se necesita)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware: limitador de tamaño de archivo
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

# Rutas API
app.include_router(files_router, prefix="", tags=["files"])


# Rutas de salud
@app.get("/healthz")
async def healthz():
    # Verifica si se puede escribir en disco
    try:
        test_file = os.path.join(settings.FILE_BASE_PATH, ".healthcheck")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {e}")

    # Verifica conexión Kafka
    try:
        test_kafka_connection()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {e}")

    return {"status": "ok"}


# Rutas de métricas
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
