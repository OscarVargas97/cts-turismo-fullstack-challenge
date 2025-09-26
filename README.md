# README.md

## Descripción

Esta aplicación es un proyecto Django con un frontend independiente. El despliegue y ejecución se realiza usando Docker y Docker Compose.
Para levantar los servicios se utiliza el script `./start.sh`.

---

## Recomendaciones

- Utilizar una distribución Linux (recomendado) con acceso al plugin oficial `docker compose` (es decir el subcomando `docker compose ...`) y no al script legacy `docker-compose`.
- Asigna permisos de ejecución al script `start.sh` antes de usarlo.

---

## Requisitos previos

- Docker (versión reciente).
- Docker Compose plugin (soporte para `docker compose`).
- Git (opcional).
- Acceso a internet para descargar imágenes y dependencias.

---

## Archivos .env

Los archivos `.env` contienen variables sensibles y deben descargarse desde los enlaces proporcionados y moverse a las carpetas correspondientes antes de arrancar el sistema.

### Enlaces

- `.env` de Django (parte 1):  
  https://send.bitwarden.com/#zkQQlv03h0aIvrNkACzt_A/bSeQS4HKYg8ny3LxMbiQyA

- `.env` de Django (parte 2):  
  https://send.bitwarden.com/#YKBeUxS9rE6KPbNkACz6gA/7UiUsxM1CdOEzJ4dFC1uGQ

- `.env` del frontend:  
  https://send.bitwarden.com/#NjnzPjPFT0mU-bNkACx7AA/7NjH_2K5c-3TJIGJCqVx4A

**Nota:** Ubica los `.env` en la carpeta correcta:
- Backend (Django): `./backend/.env`
- Frontend: `./frontend/.env`

---

## Preparar script de arranque

Dar permisos de ejecución al script `start.sh`:

```bash
chmod +x ./start.sh
```

---

## Cómo arrancar la aplicación

Con los `.env` en su lugar y permisos de ejecución dados:

```bash
./start.sh
```

Esto construirá y levantará los contenedores definidos en `docker-compose.yml`.

---

## Usuario Superadmin

Al primer arranque ya tendrás creado un usuario administrador:

```
Email:    adminuser@gmail.com
Password: Password123
```

Puedes usar estas credenciales para acceder al **Django Admin** en:  
http://localhost:8000/admin/

(ajusta el puerto si cambiaste el mapeo en tu `docker-compose.yml`).

---

## Comandos útiles (Docker / Compose)

Levantar servicios manualmente:

```bash
docker compose up -d
```

Ver logs:

```bash
docker compose logs -f
```

Migraciones:

```bash
docker compose exec backend python manage.py migrate
```

Crear superusuario adicional:

```bash
docker compose exec backend python manage.py createsuperuser
```

---

## Puertos por defecto

- Backend (Django): `8000`
- Frontend: `3000` o `80` (según configuración)
- Base de datos (Postgres): `5432`

---

## Seguridad

- No subir los `.env` al repositorio.
- Cambia las credenciales por defecto del superadmin en entornos productivos.
