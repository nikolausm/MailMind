# Produktiv-Deployment

## Inhaltsverzeichnis / Table of Contents

### In diesem Dokument
- [Übersicht](#übersicht)
- [Infrastruktur-Anforderungen](#infrastruktur-anforderungen)
  - [Mindestanforderungen](#mindestanforderungen)
  - [Empfohlene Anforderungen](#empfohlene-anforderungen)
- [Deployment-Optionen](#deployment-optionen)
  - [1. Docker-Deployment](#1-docker-deployment)
  - [2. Kubernetes-Deployment](#2-kubernetes-deployment)
  - [3. Cloud-Plattform-Deployment](#3-cloud-plattform-deployment)
- [Umgebungskonfiguration](#umgebungskonfiguration)
  - [Produktiv-Umgebungsvariablen](#produktiv-umgebungsvariablen)
- [Sicherheitshärtung](#sicherheitshärtung)
  - [SSL/TLS-Konfiguration](#ssltls-konfiguration)
  - [Sicherheits-Header](#sicherheits-header)
- [Datenbank-Setup](#datenbank-setup)
  - [PostgreSQL-Konfiguration](#postgresql-konfiguration)
  - [Migrationen](#migrationen)
- [Überwachung](#überwachung)
  - [Gesundheitsprüfungen](#gesundheitsprüfungen)
  - [Protokollierung](#protokollierung)
  - [Metriken](#metriken)
- [Backup und Wiederherstellung](#backup-und-wiederherstellung)
  - [Automatische Backups](#automatische-backups)
  - [Notfall-Wiederherstellung](#notfall-wiederherstellung)
- [Performance-Optimierung](#performance-optimierung)
  - [Caching-Strategie](#caching-strategie)
  - [Load Balancing](#load-balancing)
- [Wartung](#wartung)
  - [Zero-Downtime-Deployment](#zero-downtime-deployment)
  - [Rollback-Verfahren](#rollback-verfahren)

### Verwandte Dokumente
- [Entwicklungsumgebung](./development.md)
- [Docker-Konfiguration](./docker.md)
- [REST API-Endpunkte](../api/endpoints.md)
- [API-Fehlercodes](../api/errors.md)

---

## Übersicht
Produktiv-Deployment-Anleitung für die MailMind-Anwendung.

## Infrastruktur-Anforderungen

### Mindestanforderungen
- **CPU**: 2 vCPUs
- **RAM**: 4GB
- **Speicher**: 20GB SSD
- **Datenbank**: PostgreSQL 14+ (managed)
- **Cache**: Redis 6+ (managed)

### Empfohlene Anforderungen
- **CPU**: 4 vCPUs
- **RAM**: 8GB
- **Speicher**: 50GB SSD
- **CDN**: CloudFlare/CloudFront
- **Load Balancer**: Application Load Balancer

## Deployment-Optionen

### 1. Docker-Deployment

#### Images erstellen
```bash
# Backend
docker build -t mailmind-backend:latest -f docker/backend/Dockerfile .

# Frontend
docker build -t mailmind-frontend:latest -f docker/frontend/Dockerfile .
```

#### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    image: mailmind-backend:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    ports:
      - "9000:9000"
    
  frontend:
    image: mailmind-frontend:latest
    environment:
      - VITE_API_URL=${API_URL}
    ports:
      - "3000:3000"
```

### 2. Kubernetes-Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mailmind-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mailmind-backend
  template:
    metadata:
      labels:
        app: mailmind-backend
    spec:
      containers:
      - name: backend
        image: mailmind-backend:latest
        ports:
        - containerPort: 9000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: mailmind-secrets
              key: database-url
```

### 3. Cloud-Plattform-Deployment

#### AWS
```bash
# Mit AWS CDK deployen
cdk deploy MailMindStack

# Oder mit Terraform
terraform apply
```

#### Google Cloud
```bash
# Zu Cloud Run deployen
gcloud run deploy mailmind-backend \
  --image gcr.io/project/mailmind-backend \
  --platform managed
```

#### Azure
```bash
# Zu Azure Container Instances deployen
az container create \
  --resource-group mailmind \
  --name mailmind-backend \
  --image mailmind-backend:latest
```

## Umgebungskonfiguration

### Produktiv-Umgebungsvariablen
```bash
# Anwendung
NODE_ENV=production
API_URL=https://api.mailmind.com

# Datenbank
DATABASE_URL=postgresql://user:pass@host:5432/mailmind
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://host:6379
REDIS_PASSWORD=sicheres_passwort

# Sicherheit
JWT_SECRET=<sicheres-secret-generieren>
ENCRYPTION_KEY=<encryption-key-generieren>

# OAuth
GOOGLE_CLIENT_ID=prod_client_id
GOOGLE_CLIENT_SECRET=prod_secret

# KI-Services
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
NEW_RELIC_LICENSE_KEY=...
```

## Sicherheitshärtung

### SSL/TLS-Konfiguration
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### Sicherheits-Header
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["mailmind.com"])
app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

## Datenbank-Setup

### PostgreSQL-Konfiguration
```sql
-- Performance-Tuning
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET effective_cache_size = '3GB';
ALTER SYSTEM SET maintenance_work_mem = '256MB';

-- Produktivdatenbank erstellen
CREATE DATABASE mailmind_production;
CREATE USER mailmind_user WITH ENCRYPTED PASSWORD 'sicheres_passwort';
GRANT ALL PRIVILEGES ON DATABASE mailmind_production TO mailmind_user;
```

### Migrationen
```bash
# Migrationen ausführen
alembic upgrade head

# Backup vor Migration
pg_dump mailmind_production > backup.sql
```

## Überwachung

### Gesundheitsprüfungen
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": os.getenv("APP_VERSION")
    }

@app.get("/ready")
async def readiness_check():
    # Datenbank prüfen
    # Redis prüfen
    # Externe Services prüfen
    return {"ready": True}
```

### Protokollierung
```python
import structlog

logger = structlog.get_logger()

# Strukturierte Protokollierung
logger.info("request_received", 
    method=request.method,
    path=request.url.path,
    user_id=user_id
)
```

### Metriken
```python
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Gesamt HTTP-Anfragen')
request_duration = Histogram('http_request_duration_seconds', 'HTTP-Anfragedauer')
```

## Backup und Wiederherstellung

### Automatische Backups
```bash
# Datenbank-Backup-Skript
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://mailmind-backups/
```

### Notfall-Wiederherstellung
1. Regelmäßige automatische Backups
2. Point-in-time-Wiederherstellung
3. Multi-Region-Replikation
4. Backup-Test-Verfahren

## Performance-Optimierung

### Caching-Strategie
- Redis für Session-Speicherung
- CDN für statische Assets
- API-Response-Caching
- Datenbank-Query-Caching

### Load Balancing
```nginx
upstream backend {
    least_conn;
    server backend1:9000;
    server backend2:9000;
    server backend3:9000;
}
```

## Wartung

### Zero-Downtime-Deployment
1. Blue-Green-Deployment
2. Rolling Updates
3. Canary Releases
4. Feature Flags

### Rollback-Verfahren
```bash
# Kubernetes Rollback
kubectl rollout undo deployment/mailmind-backend

# Docker Rollback
docker service update --rollback mailmind-backend
```