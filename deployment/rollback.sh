#!/usr/bin/env bash
# Rollback de la app a una version de imagen previa.
# Uso (en el servidor de produccion):
#   ./rollback.sh v3
#
# Aprovecha el versionado por IMAGE_TAG: cambia el tag en .env y redeploya.
# Para ver versiones disponibles en el registry:
#   curl -u admin:PASS https://registry.formabelleza.com/v2/cargasdeployment2025/tags/list

set -euo pipefail

TAG="${1:?Uso: ./rollback.sh <tag, ej: v3>}"
DEPLOY_PATH="${DEPLOY_PATH:-/home/ubuntu/cargasdeployment2025}"

cd "$DEPLOY_PATH"

echo ">> Revirtiendo a IMAGE_TAG=${TAG}"
if grep -q '^IMAGE_TAG=' .env; then
    sed -i "s|^IMAGE_TAG=.*|IMAGE_TAG=${TAG}|" .env
else
    echo "IMAGE_TAG=${TAG}" >> .env
fi

docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d

echo ">> Listo. Version activa:"
docker ps --format '{{.Names}} | {{.Image}}' | grep cargas_academicas_app || true
