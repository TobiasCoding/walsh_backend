## IMPORTANTE:

---

**EJECUTAR POR DEFAULT AL INICIO**
```
docker network create walsh_net                                             #LEVANTAR RED DE DOCKER
docker ps                                                                   #CHEQUEAR CONTENEDORES UP
cd /home/admin1/Desktop/proyectos_de_desarrollo/walsh/backend               #MOVER AL DIRECTORIO PRINCIPAL DEL PROYECTO
docker compose -f ./services/kafka/docker-compose.yml down --remove-orphans #MATAR CONTENEDORES PREVIOS
docker compose -f ./services/kafka/docker-compose.yml up -d                 #LEVANTAR KAFKA, KAFKA-UI Y ZOOKEEPER
./services/kafka/create_topics.sh                                           #CREAR TOPICS DE KAFKA, CHEQUEO EN http://localhost:8080/ui/clusters/local/all-topics

```

---
---
---

**LEVANTAR KAFKA, KAFKA UI Y ZOOKEEPER**
docker compose -f services/kafka/docker-compose.yml up -d

**VER KAFKA UI**
http://localhost:8080

---

**LAUNCH MICROSERVICE**
*En la carpeta del directorio del microservicio:*

docker compose build
docker compose up -d

**DOWN MICROSERVICE**
docker compose down

---

**CONCEPTOS IMPORTANTES**

app_server simplemente llama por HTTP a search_service, No consume mensajes de Kafka. Kafka se usa para ingestión de datos y eventos asincrónicos, no para queries síncronas de usuario.

---

Ejecutar docker desde la raiz del proyecto, por ejemplo:

docker compose -f services/kafka/docker-compose.kafka.yml up -d
docker compose -f services/elasticsearch/docker-compose.elasticsearch.yml up -d

---

Para que search_service o cualquier otro microservicio pueda acceder a los contenedores de Kafka y Elasticsearch, asegurate de que todos estén en la misma network: definida en sus respectivos docker-compose.yml.

networks:

- internal

networks:
internal:
external: true

Y una sola vez creás esa red global:
docker network create internal
