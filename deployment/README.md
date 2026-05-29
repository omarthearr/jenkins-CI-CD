# Carpeta `deployment` — archivos de despliegue de produccion

Esta rama/carpeta agrupa los artefactos de despliegue de **Cargas Academicas** (servidor de produccion `54.235.105.252`).

| Archivo | Para que sirve |
|---|---|
| `docker-compose.yml` | Compose de produccion (app + db). La imagen usa `${IMAGE_TAG}` para deploy versionado. Equivale al `docker-compose.prod.yml` que vive en `/home/ubuntu/cargasdeployment2025`. |
| `.env.example` | Plantilla de variables. El `.env` real (con secretos) **no se versiona**; vive solo en el servidor. |
| `nginx-cargas-academicas.conf` | Reverse proxy de la app (dominio `cargas-academicas.formabelleza.com`). El TLS lo gestiona certbot. |
| `rollback.sh` | Revierte la app a una version de imagen previa: `./rollback.sh v3`. |

## Flujo de deploy (resumen)
El pipeline de Jenkins (rama `main`, `Jenkinsfile`) construye la imagen, la sube al registry privado (`172.31.29.90:5000`) con tag `vN` + `latest`, y por SSH al server de produccion fija `IMAGE_TAG=vN` en `.env` y hace `docker compose pull && up -d`.

## Rollback manual
```bash
ssh -i llave-django.pem ubuntu@54.235.105.252
cd /home/ubuntu/cargasdeployment2025
~/deployment/rollback.sh v3   # o el tag que quieras
```
