from fastapi import APIRouter, HTTPException, status
from app.schemas import ConfigPayload
from app.kafka_producer import publish_config_update

router = APIRouter()


@router.post("/{service_name}", status_code=status.HTTP_200_OK)
async def update_config(service_name: str, body: ConfigPayload):
    """
    Endpoint: POST /config/{service_name}
    Recibe JSON {"version": int, "payload": { key: value, ... }}.
    Publica un mensaje en Kafka para que el microservicio 'service_name'
    reciba en tiempo real la configuración.
    """
    try:
        publish_config_update(
            service=service_name, version=body.version, payload=body.payload
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al publicar actualización de configuración: {e}",
        )

    return {"detail": f"Configuración enviada para servicio '{service_name}'"}
