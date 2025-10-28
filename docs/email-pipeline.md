# E-Mail-Verarbeitungs-Pipeline

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Pipeline-Stufen](#pipeline-stufen)
- [Pipeline-Charakteristika](#pipeline-charakteristika)
  - [Technische Eigenschaften](#technische-eigenschaften)
  - [Datenfluss-Garantien](#datenfluss-garantien)
- [1. E-Mail-Erfassung](#1-e-mail-erfassung)
  - [Eingangspunkte](#eingangspunkte)
  - [Implementierung](#implementierung)
- [2. Vorverarbeitung](#2-vorverarbeitung)
- [3. KI-Verarbeitung](#3-ki-verarbeitung)
  - [Pipeline-Integration mit Agenten](#pipeline-integration-mit-agenten)
  - [Parallelisierungs-Strategie](#parallelisierungs-strategie)
- [4. Speicher-Strategie](#4-speicher-strategie)
  - [Datenbank-Schema](#datenbank-schema)
- [5. Indizierung](#5-indizierung)
- [6. Echtzeit-Updates](#6-echtzeit-updates)
- [Pipeline-Metriken](#pipeline-metriken)
  - [Performance-KPIs](#performance-kpis)
  - [Monitoring-Dashboard](#monitoring-dashboard)
- [Fehlerbehandlung](#fehlerbehandlung)
  - [Retry-Strategie](#retry-strategie)
  - [Dead Letter Queue](#dead-letter-queue)
- [Skalierungs-Strategie](#skalierungs-strategie)
  - [Horizontale Skalierung](#horizontale-skalierung)
  - [Vertikale Optimierung](#vertikale-optimierung)

## In diesem Dokument

- **[Übersicht](#übersicht)**: Einführung in die E-Mail-Verarbeitungs-Pipeline
- **[Pipeline-Stufen](#pipeline-stufen)**: Detaillierter Verarbeitungsfluss
- **[KI-Verarbeitung](#3-ki-verarbeitung)**: Integration mit dem Agent-System
- **[Speicher-Strategie](#4-speicher-strategie)**: Datenbank-Schema und Speicherung
- **[Pipeline-Metriken](#pipeline-metriken)**: Performance-KPIs und Monitoring
- **[Fehlerbehandlung](#fehlerbehandlung)**: Retry-Strategien und Dead Letter Queue
- **[Skalierungs-Strategie](#skalierungs-strategie)**: Horizontal und vertikal skalieren

## Verwandte Dokumente

- **[Agent-Architektur](./agent-architecture.md)**: Details zu den KI-Agenten
- **[KI-Agenten](./ai-agents.md)**: Detaillierte Agent-Implementierungen
- **[Vektor-Datenbank](./vector-database.md)**: Embedding-Speicherung und Suche
- **[AI-Interaktions-Regeln](./ai-interaction-rules.md)**: Interaktionsrichtlinien
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien

## Übersicht

Diese Dokumentation beschreibt den **technischen Datenfluss** der E-Mail-Verarbeitung durch das System. 

> **Siehe auch**: [Agent-Architektur](./agent-architecture.md) für Details zu den KI-Agenten

## Pipeline-Stufen

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  E-Mail-Server  │      │  WebSocket      │      │  API Upload     │
│     (IMAP)      │      │   (Echtzeit)    │      │   (REST)        │
└────────┬────────┘      └────────┬────────┘      └────────┬────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │    1. E-Mail-Erfassung    │
                    │  - IMAP-Synchronisation   │
                    │  - Push-Benachrichtigungen│
                    │  - Batch-Import           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │   2. Vorverarbeitung      │
                    │  - Struktur-Analyse       │
                    │  - Metadaten-Extraktion   │
                    │  - Inhalt-Bereinigung     │
                    │  - Anhang-Verarbeitung    │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │   3. KI-Verarbeitung      │
                    │     (Parallel)            │
                    └─────────────┬─────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │Klassifizierung│  │   Tagging    │  │  Embeddings  │
        │  - Kategorie  │  │ - Hierarchie │  │ - Vektoren   │
        │  - Priorität  │  │ - Kontext    │  │ - Semantik   │
        └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
                │                 │                 │
                └─────────────────┼─────────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │  4. Speicherung           │
                    │  - PostgreSQL (Metadaten) │
                    │  - Vektor-DB (Embeddings) │
                    │  - Redis (Cache)          │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │  5. Indizierung           │
                    │  - Volltext-Index         │
                    │  - Vektor-Index           │
                    │  - Tag-Index              │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │  6. Benachrichtigungen    │
                    │  - WebSocket Updates      │
                    │  - API Responses          │
                    │  - Event Notifications    │
                    └───────────────────────────┘
```

## Pipeline-Charakteristika

### Technische Eigenschaften
- **Asynchrone Verarbeitung**: Non-blocking I/O mit asyncio
- **Fehlertoleranz**: Exponential Backoff, Circuit Breaker
- **Skalierbarkeit**: Horizontal via Kubernetes, Vertikal via Worker-Pools
- **Monitoring**: Prometheus-Metriken, OpenTelemetry-Tracing

### Datenfluss-Garantien
```yaml
Ordering: FIFO innerhalb eines Accounts
Delivery: At-least-once mit Idempotenz
Consistency: Eventually Consistent
Durability: Persistent Queue mit Acknowledgment
```

## 1. E-Mail-Erfassung

### Eingangspunkte
- **IMAP-Integration**: 
  - Periodisches Polling (konfigurierbar)
  - IDLE-Unterstützung für Echtzeit-Updates
  - Multi-Account-Unterstützung
  
- **WebSocket-Echtzeit**:
  - Push-Benachrichtigungen vom E-Mail-Server
  - Sofortige Verarbeitung neuer E-Mails
  
- **REST API Upload**:
  - Manuelle E-Mail-Imports
  - Batch-Uploads für Migration

### Implementierung
```python
class EmailIngestion:
    async def poll_imap(self):
        """Periodisches Abrufen neuer E-Mails"""
        while True:
            new_emails = await self.imap_client.fetch_new()
            for email in new_emails:
                await self.pipeline.process(email)
            await asyncio.sleep(self.poll_interval)
    
    async def handle_websocket(self, message):
        """Echtzeit-E-Mail-Verarbeitung"""
        email = await self.parse_notification(message)
        await self.pipeline.process(email)
```

## 2. Vorverarbeitung
```python
def preprocess_email(email: RawEmail) -> ProcessedEmail:
    # E-Mail-Struktur analysieren
    parsed = parse_email(email)
    
    # Metadaten extrahieren
    metadata = extract_metadata(parsed)
    
    # Inhalt bereinigen
    cleaned = clean_content(parsed.body)
    
    # Anhänge extrahieren
    attachments = process_attachments(parsed.attachments)
    
    return ProcessedEmail(
        metadata=metadata,
        content=cleaned,
        attachments=attachments
    )
```

## 3. KI-Verarbeitung

### Pipeline-Integration mit Agenten

```python
async def process_with_ai(email: ProcessedEmail):
    """Ruft Agent-Orchestrator für KI-Verarbeitung auf"""
    
    # Delegiere an Agent-System
    orchestrator = AgentOrchestrator()
    ai_results = await orchestrator.process_email(email)
    
    # Strukturiere Ergebnisse für Pipeline
    return {
        'classification': ai_results.classification,
        'tags': ai_results.tags,
        'embeddings': ai_results.embeddings,
        'metadata': ai_results.metadata
    }
```

> **Details zu Agenten**: Siehe [Agent-Architektur](./agent-architecture.md#agent-typen) für die Funktionsweise der einzelnen Agenten

### Parallelisierungs-Strategie

```yaml
Strategie: Fan-Out/Fan-In
Vorteile:
  - Unabhängige Agenten arbeiten parallel
  - Keine Blockierung bei einzelnen Fehlern
  - Skalierbar auf mehrere Worker
  
Implementierung:
  - asyncio.gather() für Python
  - Task.WhenAll() für C#
  - Promise.all() für JavaScript
```

## 4. Speicher-Strategie
### Datenbank-Schema
```sql
-- E-Mail-Tabelle
CREATE TABLE emails (
    id UUID PRIMARY KEY,
    message_id VARCHAR UNIQUE,
    subject TEXT,
    body TEXT,
    sender VARCHAR,
    recipients JSONB,
    classification VARCHAR,
    priority INTEGER,
    tags JSONB,
    embedding_id VARCHAR,
    created_at TIMESTAMP
);

-- Embeddings in Vektor-DB
INSERT INTO vectors (id, embedding, metadata)
VALUES (?, ?, ?);
```

## 5. Indizierung
- **Volltext-Suche**: PostgreSQL FTS
- **Vektor-Suche**: Pinecone/Weaviate
- **Hybrid-Suche**: Kombiniert Schlüsselwort- und semantische Suche

## 6. Echtzeit-Updates
```python
async def notify_clients(email_id: str, event: str):
    await websocket_manager.broadcast({
        "event": event,
        "email_id": email_id,
        "timestamp": datetime.utcnow()
    })
```

## Pipeline-Metriken

### Performance-KPIs
```yaml
Latenz:
  p50: < 500ms
  p95: < 1.5s
  p99: < 3s

Durchsatz:
  Normal: 100 E-Mails/Minute
  Burst: 500 E-Mails/Minute
  
Fehlerrate:
  Ziel: < 0.1%
  Kritisch: > 1%
```

### Monitoring-Dashboard
```python
metrics = {
    'pipeline_latency_seconds': Histogram(),
    'pipeline_throughput_rpm': Gauge(),
    'pipeline_errors_total': Counter(),
    'pipeline_stage_duration': Histogram(labels=['stage']),
    'agent_invocations': Counter(labels=['agent_type'])
}
```

## Fehlerbehandlung

### Retry-Strategie
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(TransientError)
)
async def process_with_retry(email):
    return await pipeline.process(email)
```

### Dead Letter Queue
```yaml
DLQ-Regeln:
  - Nach 3 fehlgeschlagenen Versuchen
  - Bei kritischen Validierungsfehlern
  - Manuelle Review erforderlich
  
DLQ-Verarbeitung:
  - Admin-Benachrichtigung
  - Fehler-Analyse
  - Manuelles Retry möglich
```

## Skalierungs-Strategie

### Horizontale Skalierung
```yaml
Worker-Pools:
  - E-Mail-Fetcher: 2-10 Instanzen
  - Preprocessor: 4-20 Instanzen  
  - AI-Worker: 8-50 Instanzen
  - Storage-Writer: 2-10 Instanzen

Auto-Scaling:
  Trigger: CPU > 70% oder Queue-Länge > 1000
  Scale-Up: +50% Instanzen
  Scale-Down: -25% Instanzen (langsamer)
```

### Vertikale Optimierung
- **Batch-Processing**: 10-50 E-Mails gleichzeitig
- **Connection-Pooling**: Wiederverwendung von DB-Verbindungen
- **Caching**: Redis für häufige Klassifizierungen
- **Async I/O**: Non-blocking Operations überall