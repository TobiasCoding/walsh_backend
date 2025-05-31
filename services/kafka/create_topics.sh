#!/usr/bin/env bash
# services/kafka/create_topics.sh
set -e

COMPOSE_FILE="services/kafka/docker-compose.yml"
TOPICS=(
  configUpdate
  logs
  fileStored
  rawDocuments
  documentEnriched
  userCreated
  keyRegistered
  chatMessage
)

docker compose -f "$COMPOSE_FILE" exec broker bash -c '
  for t in '"${TOPICS[*]}"'; do
    kafka-topics --bootstrap-server broker:29092 \
      --create --if-not-exists --topic "$t" \
      --partitions 1 --replication-factor 1
  done
'
echo "✅ Topics creados (o ya existían)"
