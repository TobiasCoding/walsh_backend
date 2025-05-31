# servers/admin_panel/app/main.py
# Ajustado para usar la nueva convención de topics “config-<service>”

from fastapi import FastAPI
from app.kafka_producer import (
    init_kafka_producer,
    publish_config_update,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)
from app.config.env_loader import load_config_for
from app.routers.config import router as config_router

app = FastAPI(title="admin_panel")

# Lista de micro-servicios a los que se les envía su configuración.
# NO incluyas el prefijo “config-”; publish_config_update() lo agrega.
SERVICES = [
    "file_storage_service",
    "search_service",
    "user_service",
    "app_server",
    "admin_panel",
    "gpu_server",
    "api_worker",
    "crawler_worker",
    "enrichment_worker",
    "structured_worker",
]
# "log_service",


@app.on_event("startup")
def startup_event():
    """
    1. Inicializa el productor Kafka.
    2. Para cada servicio carga su JSON y publica en “config-<service>”.
    """
    try:
        init_kafka_producer()  # :contentReference[oaicite:0]{index=0}
        for service in SERVICES:
            config = load_config_for(service)
            publish_config_update(service=service, version=1, payload=config)
            print(f"[INFO] Configuración enviada a '{service}'")
    except Exception as e:
        print(f"[WARNING] Error al publicar configuraciones: {e}")


# Rutas REST del admin_panel
app.include_router(config_router, prefix="/config", tags=["config"])


@app.get("/healthz")
async def healthz():
    """Health check simple con detalles de Kafka."""
    return {
        "status": "ok",
        "kafka_bootstrap": KAFKA_BOOTSTRAP_SERVERS,
        "example_topic": KAFKA_TOPIC,
    }
