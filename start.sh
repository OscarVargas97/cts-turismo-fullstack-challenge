#!/bin/bash

if ! command -v docker &> /dev/null; then
    echo "Error: docker no está instalado o no está en el PATH."
    exit 1
fi

if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "Error: no se encontró ni 'docker compose' ni 'docker-compose'."
    exit 1
fi

$COMPOSE_CMD \
  -f backend/docker-compose.yml \
  -f frontend/docker-compose.yml \
  --project-name "${PROJECT_NAME:-myapp}" \
  up -d