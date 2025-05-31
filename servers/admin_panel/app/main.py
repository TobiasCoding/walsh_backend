from fastapi import FastAPI, HTTPException
from app.routers.config import router as config_router
from app.kafka_producer import (
    init_kafka_producer,
    test_kafka_connection,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
)

app = FastAPI(title="admin_panel")


@app.on_event("startup")
def startup_event():
    """
    Al iniciar, levantamos el Producer y verificamos que el topic exista.
    Si Kafka no está disponible o el topic no se creó aún, solo se imprime el error.
    """
    try:
        init_kafka_producer()
        test_kafka_connection()
    except Exception as e:
        print(
            f"[WARNING] No se pudo conectar a Kafka o crear topic '{KAFKA_TOPIC}': {e}"
        )


app.include_router(config_router, prefix="/config", tags=["config"])


@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "kafka_bootstrap": KAFKA_BOOTSTRAP_SERVERS,
        "kafka_topic": KAFKA_TOPIC,
    }
