**EJECUTAR POR DEFAULT AL INICIO**
```
docker ps #CHEQUEAR CONTENEDORES UP
cd /home/admin1/Desktop/proyectos_de_desarrollo/walsh/backend  #MOVER AL DIRECTORIO PRINCIPAL DEL PROYECTO
docker compose -f ./services/kafka/docker-compose.yml down --remove-orphans #MATAR CONTENEDORES PREVIOS
docker compose -f ./services/kafka/docker-compose.yml up -d #LEVANTAR KAFKA, KAFKA-UI Y ZOOKEEPER
./services/kafka/create_topics.sh #CREAR TOPICS
```

**CONTENEDORES UP DE DOCKER**
docker ps

**MATAR CONTENEDORES**
docker compose -f ./services/kafka/docker-compose.yml down --remove-orphans

**LEVANTAR KAFKA, KAFKA UI Y ZOOKEEPER**
docker compose -f ./services/kafka/docker-compose.yml up -d

**VER KAFKA UI**
http://localhost:8080


**VER LOGS DEL CONTENEDOR KAFKA: SI HAY ERROR, DEBE DECIRLO ACA**
docker compose -f ./services/kafka/docker-compose.yml logs kafka


**LEVANTAR RED DE DOCKER**
docker network create walsh_net


**LAUNCH MICROSERVICE**
*En la carpeta del directorio del microservicio:*

docker compose build
docker compose up -d