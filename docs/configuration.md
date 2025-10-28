# Konfigurationsanleitung

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Übersicht](#übersicht)
- [Umgebungsvariablen](#umgebungsvariablen)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Erweiterte Konfiguration](#erweiterte-konfiguration)
- [Konfiguration pro Umgebung](#konfiguration-pro-umgebung)
- [Konfiguration validieren](#konfiguration-validieren)
- [Häufige Konfigurationsprobleme](#häufige-konfigurationsprobleme)
- [Best Practices](#best-practices)

### Verwandte Dokumente
- [⚡ Schnellstart](./quick-start.md) - Schnelle Einrichtung
- [📥 Installation](./installation.md) - Detaillierte Installationsanleitung
- [📘 Benutzerhandbuch](./user-guide.md) - Bedienungsanleitung
- [🔙 Backend-Architektur](./backend-architecture.md) - Server-Architektur
- [🚀 Production Deployment](./deployment/production.md) - Produktionsumgebung

## Übersicht

Diese Anleitung beschreibt alle Konfigurationsmöglichkeiten für MailMind.

## Umgebungsvariablen

### Erforderliche Variablen

Erstellen Sie eine `.env`-Datei im Projekt-Hauptverzeichnis:

```bash
cp .env.example .env
```

#### LLM-Provider

```env
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus-20240229
```

#### Vektor-Datenbank

```env
# Pinecone
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=mailmind-embeddings

# Oder Weaviate
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=...
```

#### Datenbank

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/mailmind
REDIS_URL=redis://localhost:6379
```

#### E-Mail-Server

```env
# Standard IMAP/SMTP
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

## Konfigurationsdateien

### KI-Einstellungen

`config/ai_settings.yaml`:

```yaml
# Klassifizierung
classification:
  enabled: true
  model: "gpt-3.5-turbo"
  confidence_threshold: 0.7
  categories:
    - persönlich
    - arbeit
    - werbung
    - newsletter
    - benachrichtigung
    - spam
  
# Tagging
tagging:
  enabled: true
  model: "gpt-3.5-turbo"
  max_tags: 5
  hierarchical: true
  min_confidence: 0.6
  
# Zusammenfassung
summarization:
  enabled: true
  model: "gpt-4"
  max_length: 200
  style: "bullet_points"  # oder "paragraph"
  
# Antwort-Vorschläge
response_suggestions:
  enabled: false
  model: "gpt-4"
  max_suggestions: 3
  tone_options:
    - formell
    - informell
    - freundlich
    - geschäftlich
```

### E-Mail-Synchronisation

`config/sync_settings.yaml`:

```yaml
# IMAP-Einstellungen
imap:
  poll_interval: 300  # Sekunden
  batch_size: 50
  max_retry: 3
  use_idle: true  # IDLE-Befehl für Echtzeit
  
# Synchronisation
sync:
  frequency: "5min"  # oder "realtime", "hourly", "daily"
  depth_days: 30  # Wie viele Tage zurück
  initial_import: 7  # Tage beim ersten Import
  auto_categorize: true
  process_attachments: true
  max_attachment_size: 10485760  # 10MB
  
# WebSocket
websocket:
  enabled: true
  reconnect_interval: 5  # Sekunden
  max_reconnect_attempts: 10
```

### Server-Konfiguration

`config/server.yaml`:

```yaml
# Backend API
api:
  host: "0.0.0.0"
  port: 9000
  workers: 4
  cors_origins:
    - "http://localhost:3000"
    - "http://localhost:5000"
  rate_limit: "100/minute"
  
# Frontend
frontend:
  host: "localhost"
  port: 3000
  hot_reload: true
  
# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "logs/mailmind.log"
  max_size: "10MB"
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Sicherheitseinstellungen

`config/security.yaml`:

```yaml
# Authentifizierung
auth:
  jwt_secret_key: "CHANGE_THIS_TO_RANDOM_SECRET"
  jwt_algorithm: "HS256"
  access_token_expire: 30  # Minuten
  refresh_token_expire: 7  # Tage
  password_min_length: 8
  require_email_verification: true
  
# Verschlüsselung
encryption:
  algorithm: "AES-256-GCM"
  key_derivation: "PBKDF2"
  iterations: 100000
  
# Rate Limiting
rate_limiting:
  enabled: true
  default: "100/hour"
  api_endpoints:
    search: "20/minute"
    send_email: "10/minute"
    ai_process: "50/hour"
```

## Erweiterte Konfiguration

### Multi-Tenant-Setup

Für mehrere Benutzer oder Organisationen:

```yaml
# config/multi_tenant.yaml
tenancy:
  enabled: true
  isolation_level: "database"  # oder "schema", "row"
  max_users_per_tenant: 100
  storage_quota_gb: 50
```

### Cache-Konfiguration

```yaml
# config/cache.yaml
cache:
  provider: "redis"
  ttl:
    search_results: 300  # Sekunden
    email_classifications: 86400  # 1 Tag
    embeddings: 604800  # 1 Woche
  max_memory: "256MB"
```

### Performance-Tuning

```yaml
# config/performance.yaml
performance:
  # Batch-Verarbeitung
  batch_processing:
    enabled: true
    size: 50
    parallel_workers: 4
    
  # Vektor-Suche
  vector_search:
    max_results: 100
    similarity_threshold: 0.7
    use_cache: true
    
  # Datenbank
  database:
    connection_pool_size: 20
    statement_timeout: 30000  # ms
    query_timeout: 10000  # ms
```

## Konfiguration pro Umgebung

### Entwicklung

```bash
# .env.development
NODE_ENV=development
API_URL=http://localhost:9000
DEBUG=true
LOG_LEVEL=DEBUG
```

### Produktion

```bash
# .env.production
NODE_ENV=production
API_URL=https://api.mailmind.com
DEBUG=false
LOG_LEVEL=WARNING
USE_SSL=true
```

## Konfiguration validieren

Prüfen Sie Ihre Konfiguration:

```bash
# Konfiguration testen
python scripts/validate_config.py

# Umgebungsvariablen prüfen
python scripts/check_env.py
```

## Häufige Konfigurationsprobleme

### API-Schlüssel fehlen

```bash
# Fehler
Error: OPENAI_API_KEY not found in environment

# Lösung
export OPENAI_API_KEY="sk-..."
```

### Datenbankverbindung fehlgeschlagen

```bash
# Fehler
psycopg2.OperationalError: could not connect to server

# Lösung - Prüfen Sie:
1. PostgreSQL läuft: sudo service postgresql status
2. Verbindungsstring korrekt: postgresql://user:pass@host:port/db
3. Firewall-Regeln
```

### Vektor-DB nicht erreichbar

```bash
# Fehler
pinecone.core.exceptions.PineconeException: API key invalid

# Lösung
1. API-Schlüssel prüfen
2. Environment korrekt
3. Index existiert
```

## Best Practices

1. **Umgebungsvariablen**: Niemals in Git committen
2. **Secrets**: Verwenden Sie einen Secret Manager in Produktion
3. **Konfigurationstrennung**: Separate Configs für dev/staging/prod
4. **Validierung**: Immer Konfiguration beim Start validieren
5. **Dokumentation**: Alle Konfigurationsänderungen dokumentieren