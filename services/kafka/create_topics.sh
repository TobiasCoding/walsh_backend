#!/usr/bin/env bash
# services/kafka/create_topics.sh
set -e

COMPOSE_FILE="services/kafka/docker-compose.yml"
TOPICS=(
  logs
  config-logs
  file-storage-service
  config-file-storage-service
  search-service
  config-search-service
  user-service
  config-user-service
  app-server
  config-app-server
  admin-panel
  config-admin-panel
  gpu-server
  config-gpu-server
  api-worker
  config-api-worker
  crawler-worker
  config-crawler-worker
  enrichment-worker
  config-enrichment-worker
  structured-worker
  config-structured-worker
)

docker compose -f "$COMPOSE_FILE" exec broker bash -c '
  for t in '"${TOPICS[*]}"'; do
    kafka-topics --bootstrap-server broker:29092 \
      --create --if-not-exists --topic "$t" \
      --partitions 1 --replication-factor 1
  done
'
echo "✅ Topics creados (o ya existían)"
