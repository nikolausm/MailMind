# Docker-Konfiguration

## Inhaltsverzeichnis / Table of Contents

### In diesem Dokument
- [Docker-Images](#docker-images)
  - [Backend-Dockerfile](#backend-dockerfile)
  - [Frontend-Dockerfile](#frontend-dockerfile)
- [Docker Compose](#docker-compose)
  - [Entwicklung](#entwicklung)
  - [Produktion](#produktion)
- [Erstellen und Ausführen](#erstellen-und-ausführen)
  - [Build-Befehle](#build-befehle)
  - [Ausführungsbefehle](#ausführungsbefehle)
- [Docker-Registry](#docker-registry)
  - [In Registry hochladen](#in-registry-hochladen)
  - [Aus Registry herunterladen](#aus-registry-herunterladen)
- [Container-Orchestrierung](#container-orchestrierung)
  - [Docker Swarm](#docker-swarm)
  - [Kubernetes](#kubernetes)
- [Optimierung](#optimierung)
  - [Multi-Stage-Builds](#multi-stage-builds)
  - [Image-Größenoptimierung](#image-größenoptimierung)
  - [Build-Cache](#build-cache)
- [Sicherheit](#sicherheit)
  - [Sicherheitsüberprüfung](#sicherheitsüberprüfung)
  - [Best Practices](#best-practices)
  - [Nicht-Root-Benutzer](#nicht-root-benutzer)
- [Debugging](#debugging)
  - [Container-Zugriff](#container-zugriff)
  - [Debug-Modus](#debug-modus)
- [Überwachung](#überwachung)
  - [Container-Statistiken](#container-statistiken)
  - [Gesundheitsprüfungen](#gesundheitsprüfungen)

### Verwandte Dokumente
- [Entwicklungsumgebung](./development.md)
- [Produktiv-Deployment](./production.md)
- [REST API-Endpunkte](../api/endpoints.md)
- [WebSocket-Ereignisse](../api/websocket.md)

---

## Docker-Images

### Backend-Dockerfile
```dockerfile
# docker/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY src/ ./src/
COPY alembic.ini .
COPY alembic/ ./alembic/

# Umgebungsvariablen setzen
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Gesundheitsprüfung
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:9000/health')"

# Anwendung ausführen
CMD ["uvicorn", "src.backend.api.main:app", "--host", "0.0.0.0", "--port", "9000"]
```

### Frontend-Dockerfile
```dockerfile
# docker/frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Paketdateien kopieren
COPY src/frontend/package*.json ./

# Abhängigkeiten installieren
RUN npm ci

# Quellcode kopieren
COPY src/frontend/ .

# Anwendung erstellen
RUN npm run build

# Produktionsstufe
FROM nginx:alpine

# Erstellte Dateien kopieren
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx-Konfiguration kopieren
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Gesundheitsprüfung
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
```

## Docker Compose

### Entwicklung
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: mailmind
      POSTGRES_USER: mailmind
      POSTGRES_PASSWORD: devpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: .
      dockerfile: docker/backend/Dockerfile
    environment:
      DATABASE_URL: postgresql://mailmind:devpassword@postgres:5432/mailmind
      REDIS_URL: redis://redis:6379
    volumes:
      - ./src:/app/src
    ports:
      - "9000:9000"
    depends_on:
      - postgres
      - redis
    command: uvicorn src.backend.api.main:app --reload --host 0.0.0.0 --port 9000

  frontend:
    build:
      context: .
      dockerfile: docker/frontend/Dockerfile.dev
    volumes:
      - ./src/frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:9000/api

volumes:
  postgres_data:
```

### Produktion
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    image: mailmind-backend:latest
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      JWT_SECRET: ${JWT_SECRET}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    ports:
      - "9000:9000"

  frontend:
    image: mailmind-frontend:latest
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
    ports:
      - "3000:3000"

  nginx:
    image: nginx:alpine
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
      - frontend
```

## Erstellen und Ausführen

### Build-Befehle
```bash
# Alle Services erstellen
docker-compose build

# Bestimmten Service erstellen
docker-compose build backend

# Ohne Cache erstellen
docker-compose build --no-cache
```

### Ausführungsbefehle
```bash
# Alle Services starten
docker-compose up

# Im Hintergrund starten
docker-compose up -d

# Bestimmten Service starten
docker-compose up backend

# Protokolle anzeigen
docker-compose logs -f backend

# Services stoppen
docker-compose down

# Stoppen und Volumes entfernen
docker-compose down -v
```

## Docker-Registry

### In Registry hochladen
```bash
# Images taggen
docker tag mailmind-backend:latest registry.example.com/mailmind-backend:latest
docker tag mailmind-frontend:latest registry.example.com/mailmind-frontend:latest

# Images hochladen
docker push registry.example.com/mailmind-backend:latest
docker push registry.example.com/mailmind-frontend:latest
```

### Aus Registry herunterladen
```bash
docker pull registry.example.com/mailmind-backend:latest
docker pull registry.example.com/mailmind-frontend:latest
```

## Container-Orchestrierung

### Docker Swarm
```bash
# Swarm initialisieren
docker swarm init

# Stack bereitstellen
docker stack deploy -c docker-compose.prod.yml mailmind

# Service skalieren
docker service scale mailmind_backend=5

# Service aktualisieren
docker service update --image mailmind-backend:v2 mailmind_backend
```

### Kubernetes
Siehe [Kubernetes-Deployment-Anleitung](./production.md#kubernetes-deployment)

## Optimierung

### Multi-Stage-Builds
- Image-Größe reduzieren
- Build- und Laufzeitabhängigkeiten trennen
- Cache-Layer-Optimierung

### Image-Größenoptimierung
```dockerfile
# Alpine-Images verwenden
FROM python:3.11-alpine

# Unnötige Dateien entfernen
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache /tmp/*
```

### Build-Cache
```bash
# BuildKit für besseres Caching verwenden
DOCKER_BUILDKIT=1 docker build .

# Cache-Mount verwenden
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

## Sicherheit

### Sicherheitsüberprüfung
```bash
# Nach Schwachstellen scannen
docker scan mailmind-backend:latest

# Trivy verwenden
trivy image mailmind-backend:latest
```

### Best Practices
1. Nicht als Root ausführen
2. Offizielle Basis-Images verwenden
3. Versionen festlegen
4. Layer minimieren
5. .dockerignore verwenden
6. Keine Geheimnisse in Images speichern

### Nicht-Root-Benutzer
```dockerfile
# Nicht-Root-Benutzer erstellen
RUN addgroup -g 1000 mailmind && \
    adduser -D -u 1000 -G mailmind mailmind

USER mailmind
```

## Debugging

### Container-Zugriff
```bash
# Bash in laufendem Container ausführen
docker exec -it container_name bash

# Neuen Container mit Shell starten
docker run -it --rm mailmind-backend:latest sh
```

### Debug-Modus
```yaml
# docker-compose.debug.yml
services:
  backend:
    command: python -m pdb src/backend/api/main.py
    stdin_open: true
    tty: true
```

## Überwachung

### Container-Statistiken
```bash
# Ressourcennutzung anzeigen
docker stats

# Bestimmten Container anzeigen
docker stats container_name
```

### Gesundheitsprüfungen
```bash
# Gesundheitsstatus prüfen
docker inspect --format='{{.State.Health.Status}}' container_name

# Gesundheitsprüfungsprotokolle anzeigen
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' container_name
```