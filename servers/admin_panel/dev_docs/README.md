# admin_panel

Microservicio para gestionar configuración centralizada vía Kafka.

## Requisitos previos

- Python 3.10+
- Docker (solo para Kafka y Zookeeper)

## 1. Levantar Kafka y Zookeeper en Docker

```bash
# Desde la raíz del proyecto (o donde esté tu docker-compose.yml)
docker network create walsh_net         # si no existe
docker compose -f services/kafka/docker-compose.yml up -d
```
