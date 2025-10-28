# KI-Agenten Dokumentation

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Agenten-Architektur](#agenten-architektur)
  - [Orchestrierung](#orchestrierung)
  - [Verarbeitungsfluss](#verarbeitungsfluss)
- [Kern-Agenten](#kern-agenten)
  - [EmailClassifierAgent](#emailclassifieragent)
  - [TaggingAgent](#taggingagent)
  - [SearchAgent](#searchagent)
- [Bedarfsbasierte Agenten](#bedarfsbasierte-agenten)
  - [SummaryAgent](#summaryagent)
  - [ResponseAgent](#responseagent)
- [Agent-Interaktion](#agent-interaktion)
  - [Kommunikationsprotokoll](#kommunikationsprotokoll)
  - [Fehlerbehandlung](#fehlerbehandlung)
- [Performance-Optimierung](#performance-optimierung)
  - [Parallelisierung](#parallelisierung)
  - [Caching-Strategie](#caching-strategie)
  - [Batch-Verarbeitung](#batch-verarbeitung)
- [Monitoring und Metriken](#monitoring-und-metriken)
  - [Agent-Metriken](#agent-metriken)
  - [Health Checks](#health-checks)
- [Erweiterung und Anpassung](#erweiterung-und-anpassung)
  - [Neuen Agent hinzufügen](#neuen-agent-hinzufügen)
  - [Modell-Fine-Tuning](#modell-fine-tuning)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
  - [Häufige Probleme](#häufige-probleme)

## In diesem Dokument

- **[Übersicht](#übersicht)**: Einführung in das Multi-Agenten-System
- **[Agenten-Architektur](#agenten-architektur)**: Architektur und Orchestrierung
- **[Kern-Agenten](#kern-agenten)**: Classifier, Tagging und Search Agenten
- **[Bedarfsbasierte Agenten](#bedarfsbasierte-agenten)**: Summary und Response Agenten
- **[Performance-Optimierung](#performance-optimierung)**: Parallelisierung und Caching
- **[Monitoring](#monitoring-und-metriken)**: Metriken und Health Checks
- **[Erweiterung](#erweiterung-und-anpassung)**: Neue Agenten hinzufügen

## Verwandte Dokumente

- **[Agent-Architektur](./agent-architecture.md)**: Detaillierte Architektur-Übersicht
- **[E-Mail-Pipeline](./email-pipeline.md)**: Technischer Verarbeitungsfluss
- **[AI-Interaktions-Regeln](./ai-interaction-rules.md)**: Interaktionsrichtlinien
- **[Vektor-Datenbank](./vector-database.md)**: Such-Integration
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien

## Übersicht

MailMind nutzt ein ausgeklügeltes Multi-Agenten-System zur intelligenten E-Mail-Verarbeitung. Jeder Agent ist auf eine spezifische Aufgabe spezialisiert und arbeitet im Orchestrierungsframework zusammen.

## Agenten-Architektur

### Orchestrierung

Der `AgentOrchestrator` koordiniert alle Agenten:

```python
class AgentOrchestrator:
    def __init__(self):
        self.core_agents = {
            'classifier': EmailClassifierAgent(),
            'tagger': TaggingAgent(),
            'search': SearchAgent()
        }
        self.on_demand_agents = {
            'summary': SummaryAgent(),
            'response': ResponseAgent()
        }
```

### Verarbeitungsfluss

```
E-Mail → Orchestrator → Parallele Agenten → Aggregation → Speicherung
```

## Kern-Agenten

### EmailClassifierAgent

**Zweck**: Klassifiziert E-Mails in vordefinierte Kategorien und weist Prioritäten zu.

#### Konfiguration

```python
class EmailClassifierAgent:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.categories = [
            "persönlich",
            "arbeit", 
            "werbung",
            "newsletter",
            "benachrichtigung",
            "spam"
        ]
        self.confidence_threshold = 0.7
```

#### Eingabe/Ausgabe

```python
# Eingabe
{
    "subject": "Meeting morgen um 10 Uhr",
    "sender": "chef@firma.de",
    "body": "Bitte bereiten Sie die Präsentation vor..."
}

# Ausgabe
{
    "category": "arbeit",
    "priority": "hoch",
    "confidence": 0.92,
    "reasoning": "Geschäftlicher Absender, Meeting-Bezug"
}
```

#### Klassifizierungslogik

1. **Absender-Analyse**: Domain und bekannte Kontakte
2. **Betreff-Analyse**: Schlüsselwörter und Muster
3. **Inhalt-Analyse**: Themen und Tonfall
4. **Kontext-Analyse**: Vorherige Interaktionen

### TaggingAgent

**Zweck**: Generiert hierarchische Tags basierend auf E-Mail-Inhalt.

#### Konfiguration

```python
class TaggingAgent:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.max_tags = 5
        self.hierarchical = True
        self.min_confidence = 0.6
```

#### Tag-Hierarchie

```
Projekt
├── Projekt Alpha
│   ├── Phase 1
│   ├── Phase 2
│   └── Abschluss
├── Projekt Beta
└── Projekt Gamma

Kunde
├── Wichtige Kunden
│   ├── Kunde A
│   └── Kunde B
└── Neue Kunden
```

#### Eingabe/Ausgabe

```python
# Eingabe
{
    "subject": "Projekt Alpha - Phase 2 Update",
    "body": "Die Entwicklung ist zu 80% abgeschlossen..."
}

# Ausgabe
{
    "tags": [
        {
            "path": "Projekt/Projekt Alpha/Phase 2",
            "confidence": 0.95
        },
        {
            "path": "Status/In Bearbeitung",
            "confidence": 0.88
        },
        {
            "path": "Priorität/Mittel",
            "confidence": 0.75
        }
    ]
}
```

### SearchAgent

**Zweck**: Ermöglicht semantische Suche durch Vektor-Embeddings.

#### Konfiguration

```python
class SearchAgent:
    def __init__(self):
        self.embedding_model = "all-MiniLM-L6-v2"
        self.vector_db = "pinecone"  # oder "weaviate"
        self.similarity_threshold = 0.7
        self.max_results = 100
```

#### Embedding-Generierung

```python
def generate_embedding(self, email):
    # Kombiniere relevante Felder
    text = f"{email.subject} {email.body}"
    
    # Generiere Embedding
    embedding = self.model.encode(text)
    
    # Speichere in Vektor-DB
    self.vector_db.upsert(
        id=email.id,
        vector=embedding,
        metadata={
            "sender": email.sender,
            "date": email.date,
            "category": email.category
        }
    )
```

#### Suchanfrage-Verarbeitung

```python
def search(self, query: str, filters: dict = None):
    # Query-Embedding
    query_vector = self.model.encode(query)
    
    # Vektor-Suche
    results = self.vector_db.search(
        vector=query_vector,
        top_k=self.max_results,
        filter=filters,
        include_metadata=True
    )
    
    # Ranking und Filterung
    return self._rank_results(results)
```

## Bedarfsbasierte Agenten

### SummaryAgent

**Zweck**: Erstellt Zusammenfassungen für lange E-Mails oder Threads.

#### Konfiguration

```python
class SummaryAgent:
    def __init__(self):
        self.model = "gpt-4"
        self.max_length = 200
        self.styles = ["bullet_points", "paragraph", "key_points"]
```

#### Zusammenfassungstypen

1. **Kurzzusammenfassung**: 2-3 Sätze
2. **Detaillierte Zusammenfassung**: Strukturierte Übersicht
3. **Aktionspunkte**: Extrahierte To-Dos
4. **Thread-Zusammenfassung**: Gesamter Verlauf

#### Eingabe/Ausgabe

```python
# Eingabe
{
    "email_id": "12345",
    "style": "bullet_points",
    "include_actions": true
}

# Ausgabe
{
    "summary": {
        "main_points": [
            "Budget-Genehmigung erforderlich",
            "Deadline: 15. Januar",
            "3 Optionen vorgeschlagen"
        ],
        "action_items": [
            "Budget-Dokument überprüfen",
            "Feedback bis Freitag senden"
        ],
        "key_decisions": [
            "Option B bevorzugt"
        ]
    }
}
```

### ResponseAgent

**Zweck**: Generiert intelligente Antwortvorschläge.

#### Konfiguration

```python
class ResponseAgent:
    def __init__(self):
        self.model = "gpt-4"
        self.max_suggestions = 3
        self.tone_options = [
            "formell",
            "informell", 
            "freundlich",
            "geschäftlich"
        ]
```

#### Antwort-Generierung

```python
def suggest_responses(self, email, context):
    prompts = []
    
    for tone in self.tone_options:
        prompt = self._build_prompt(email, context, tone)
        prompts.append(prompt)
    
    responses = self.model.generate(prompts)
    return self._format_suggestions(responses)
```

#### Eingabe/Ausgabe

```python
# Eingabe
{
    "email_id": "12345",
    "tone": "geschäftlich",
    "length": "kurz"
}

# Ausgabe
{
    "suggestions": [
        {
            "text": "Vielen Dank für Ihre Nachricht...",
            "tone": "geschäftlich",
            "confidence": 0.90
        },
        {
            "text": "Ich habe Ihre Anfrage erhalten...",
            "tone": "geschäftlich",
            "confidence": 0.85
        }
    ]
}
```

## Agent-Interaktion

### Kommunikationsprotokoll

Agenten kommunizieren über standardisierte Nachrichten:

```python
class AgentMessage:
    def __init__(self):
        self.id: str
        self.sender_agent: str
        self.receiver_agent: str
        self.message_type: str
        self.payload: dict
        self.timestamp: datetime
        self.priority: int
```

### Fehlerbehandlung

```python
class AgentErrorHandler:
    def handle_error(self, agent, error):
        if isinstance(error, TimeoutError):
            return self.get_fallback_result(agent)
        elif isinstance(error, APIError):
            return self.retry_with_backoff(agent)
        else:
            self.log_error(agent, error)
            return self.get_default_result(agent)
```

## Performance-Optimierung

### Parallelisierung

```python
async def process_parallel(email):
    tasks = [
        classifier.classify(email),
        tagger.tag(email),
        embedder.embed(email)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return aggregate_results(results)
```

### Caching-Strategie

```python
class AgentCache:
    def __init__(self):
        self.redis_client = redis.Redis()
        self.ttl = {
            'classification': 86400,  # 1 Tag
            'tags': 3600,  # 1 Stunde
            'embeddings': 604800  # 1 Woche
        }
```

### Batch-Verarbeitung

```python
def process_batch(emails, batch_size=50):
    batches = chunk_emails(emails, batch_size)
    
    for batch in batches:
        results = parallel_process(batch)
        store_results(results)
```

## Monitoring und Metriken

### Agent-Metriken

```python
class AgentMetrics:
    def track(self):
        return {
            "response_time": self.avg_response_time(),
            "success_rate": self.success_rate(),
            "error_rate": self.error_rate(),
            "throughput": self.emails_per_minute(),
            "accuracy": self.classification_accuracy()
        }
```

### Health Checks

```python
def health_check():
    status = {}
    
    for agent_name, agent in agents.items():
        status[agent_name] = {
            "alive": agent.ping(),
            "response_time": agent.test_latency(),
            "last_success": agent.last_success_time()
        }
    
    return status
```

## Erweiterung und Anpassung

### Neuen Agent hinzufügen

1. **Agent-Klasse erstellen**:
```python
class CustomAgent:
    def __init__(self):
        self.name = "custom_agent"
        self.model = "your-model"
    
    async def process(self, payload: dict) -> dict:
        # Implementierung
        pass
```

2. **Im Orchestrator registrieren**:
```python
orchestrator.register_agent('custom', CustomAgent())
```

3. **Pipeline erweitern**:
```python
def process_email_extended(email):
    standard_results = process_standard(email)
    custom_result = custom_agent.process(email)
    return merge_results(standard_results, custom_result)
```

### Modell-Fine-Tuning

```python
class ModelTrainer:
    def fine_tune(self, training_data):
        # Daten vorbereiten
        X_train, y_train = prepare_data(training_data)
        
        # Modell trainieren
        model = load_base_model()
        model.fit(X_train, y_train)
        
        # Evaluieren
        metrics = evaluate_model(model)
        
        # Speichern wenn besser
        if metrics['accuracy'] > threshold:
            save_model(model)
```

## Best Practices

### 1. Agent-Design
- Single Responsibility Principle
- Klare Input/Output-Definitionen
- Fehlertoleranz einbauen
- Timeout-Handling implementieren

### 2. Performance
- Parallelisierung wo möglich
- Intelligentes Caching
- Batch-Verarbeitung für große Mengen
- Ressourcen-Limits setzen

### 3. Monitoring
- Comprehensive Logging
- Metriken tracken
- Alerts bei Anomalien
- Regular Health Checks

### 4. Testing
```python
def test_classifier_agent():
    test_email = {
        "subject": "Test Meeting",
        "sender": "test@example.com",
        "body": "This is a test"
    }
    
    result = classifier.classify(test_email)
    
    assert result['category'] in valid_categories
    assert 0 <= result['confidence'] <= 1
    assert result['priority'] in ['niedrig', 'mittel', 'hoch']
```

## Troubleshooting

### Häufige Probleme

#### Agent antwortet nicht
```bash
# Status prüfen
curl http://localhost:9000/api/agents/status

# Logs prüfen
tail -f logs/agents.log

# Neustart
systemctl restart mailmind-agents
```

#### Niedrige Genauigkeit
- Training-Daten überprüfen
- Confidence-Threshold anpassen
- Modell-Update in Betracht ziehen
- Feature-Engineering verbessern

#### Performance-Probleme
- Batch-Size erhöhen
- Caching aktivieren
- Parallelisierung optimieren
- Ressourcen-Limits prüfen