# servers/admin_panel/app/main.py

from fastapi import FastAPI
from app.kafka_producer import (
    init_kafka_producer,
    publish_config_update,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)
from config.env_loader import load_config_for
from app.routers.config import router as config_router

app = FastAPI(title="admin_panel")

SERVICES = [
    "config-file-service",
    "config-search-service",
]  # o cargalo dinámico si querés


@app.on_event("startup")
def startup_event():
    try:
        init_kafka_producer()
        for service in SERVICES:
            config = load_config_for(service)
            publish_config_update(service=service, version=1, payload=config)
            print(f"[INFO] Configuración enviada a '{service}'")
    except Exception as e:
        print(f"[WARNING] Error al publicar configuraciones: {e}")


app.include_router(config_router, prefix="/config", tags=["config"])


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "kafka_bootstrap": KAFKA_BOOTSTRAP_SERVERS,
        "kafka_topic": KAFKA_TOPIC,
    }
