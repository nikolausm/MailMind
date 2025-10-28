ja# CLAUDE.md

Diese Datei bietet Anleitungen für Claude Code (claude.ai/code) bei der Arbeit mit Code in diesem Repository.

## Projektübersicht

MailMind ist ein intelligenter E-Mail-Client, der RAG (Retrieval-Augmented Generation) verwendet, um semantische Suche, intelligentes Auto-Tagging und KI-gestützte Einblicke bereitzustellen. Das System ist mit einer hybriden Python/React-Architektur aufgebaut.

## Entwicklungsbefehle

### Einrichtung
```bash
# Alle Abhängigkeiten installieren
npm install
pip install -r requirements.txt

# Umgebungsvariablen einrichten
cp .env.example .env  # .env mit Ihren API-Schlüsseln bearbeiten
```

### Entwicklung
```bash
# Entwicklungsserver starten (Frontend und Backend)
npm run dev

# Einzelne Services starten
npm run dev:backend    # Backend API Server
npm run dev:frontend   # Frontend React App
```

### Testen
```bash
# Python Tests ausführen 
pytest

# Spezifische Test-Datei ausführen
pytest tests/unit/test_email_classifier.py
```

### Code-Qualität
```bash
# Python Code formatieren
black src/
flake8 src/
```

## Architektur

### Multi-Sprachen-Stack
- **Frontend**: React mit TypeScript - befindet sich in `src/frontend/`
- **Backend API**: FastAPI (Python) - befindet sich in `src/backend/api/`
- **KI-Services**: Python mit LangChain - befindet sich in `src/ai/`
- **Gemeinsam**: Gemeinsame Typen und Utilities - befindet sich in `src/shared/`

### KI-Agenten-System
Die Kerninnovation ist das KI-Agenten-Orchestrierungssystem:

1. **AgentOrchestrator** (`src/ai/orchestrator.py`): Zentraler Koordinator, der alle KI-Agenten verwaltet und E-Mails durch Agenten-Pipelines verarbeitet
2. **EmailClassifierAgent** (`src/ai/agents/email_classifier.py`): Kategorisiert E-Mails und weist Prioritätsstufen zu
3. **SearchAgent** (`src/ai/agents/search_agent.py`): Verarbeitet semantische Suche mit Vektor-Embeddings
4. **TaggingAgent** (`src/ai/agents/tagging_agent.py`): Generiert automatisch hierarchische Tags
5. **SummaryAgent** und **ResponseAgent**: Für zukünftige Implementierung geplant

### E-Mail-Verarbeitungs-Pipeline
1. E-Mail-Erfassung → AgentOrchestrator.process_email()
2. Parallele Verarbeitung durch ClassifierAgent, TaggingAgent und Embedding-Generierung
3. Ergebnisse konsolidiert und mit Vektordatenbank-Integration gespeichert
4. Frontend-Abfragen durch SearchAgent für semantische Abfrage verarbeitet

## Hauptabhängigkeiten

### Python Stack
- **LangChain**: RAG-Implementierung und Agenten-Framework
- **FastAPI**: REST API Server mit Async-Unterstützung
- **Pinecone/Weaviate**: Vektordatenbank für Embeddings
- **OpenAI/Anthropic**: LLM-Anbieter für Agenten-Intelligenz

### Frontend Stack
- **React**: Mit TypeScript und Vite
- **WebSocket/SSE**: Echtzeit-Kommunikation für E-Mail-Benachrichtigungen
- **State Management**: React Context API und lokaler State

## Entwicklungsrichtlinien

### Authentifizierungsentwicklung
- **Multi-Provider-Unterstützung**: Google, Microsoft, Apple, E-Mail+Passwort
- **OAuth 2.0 Implementierung** für Social Logins
- **JWT-basiertes Session-Management** mit Refresh Tokens
- **Sichere Passwortbehandlung** mit Argon2/bcrypt
- Siehe `docs/AUTHENTICATION.md` für vollständige Anforderungen

### Agenten-Entwicklung
- Jeder Agent sollte von einer Basis-Agenten-Klasse mit standardisierter `process()`-Methode erben
- Verwenden Sie Type Hints umfassend für Python-Code (`typing` Modul)
- Agenten kommunizieren über den Orchestrator, nicht direkt
- Alle Agenten sollten strukturierte Ergebnisse mit Konfidenz-Scores zurückgeben

### API-Entwicklung
- FastAPI Endpunkte in `src/backend/api/routes/`
- Verwenden Sie Pydantic Modelle für Request/Response Validierung
- Implementieren Sie Async-Endpunkte für bessere Performance
- Befolgen Sie RESTful Konventionen

### Frontend-Entwicklung
- Komponenten in `src/frontend/components/`
- Verwenden Sie moderne komponentenbasierte Architektur
- Implementieren Sie Echtzeit-Updates mit WebSockets oder Server-Sent Events
- Befolgen Sie Best Practices für React

### Test-Strategie
- Unit-Tests für einzelne Agenten und Utilities
- Integrationstests für Agenten-Orchestrierung
- E2E-Tests für vollständige E-Mail-Verarbeitungsworkflows
- Mock externe LLM-Aufrufe in Tests

## Erforderliche Umgebungsvariablen

### KI & Datenbank
- `OPENAI_API_KEY`: Für OpenAI LLM Integration
- `ANTHROPIC_API_KEY`: Für Anthropic LLM Integration  
- `PINECONE_API_KEY`: Für Vektordatenbank
- `DATABASE_URL`: Für E-Mail-Speicher-Datenbank

### Authentifizierung (siehe docs/AUTHENTICATION.md für vollständige Details)
- `JWT_SECRET`: JWT Token Signierung
- `JWT_REFRESH_SECRET`: Refresh Token Signierung
- OAuth-Anbieter: Google, Microsoft, Apple Anmeldedaten
- E-Mail-Service-Anmeldedaten für Verifikation/Reset

## Häufige Muster

### Neuen Agenten hinzufügen
1. Agenten-Klasse in `src/ai/agents/` erstellen
2. `process(payload: Dict[str, Any])` Methode implementieren
3. Mit Orchestrator beim Startup registrieren
4. Agenten-Tasks zur E-Mail-Verarbeitungs-Pipeline hinzufügen

### Vektordatenbank-Integration
- Verwenden Sie sentence-transformers für Embedding-Generierung
- Speichern Sie Embeddings mit Metadaten in Pinecone/Weaviate
- Implementieren Sie Ähnlichkeitssuche für semantische Abfragen

## Performance-Überlegungen
- Agenten-Verarbeitung ist für parallele Ausführung konzipiert
- Verwenden Sie async/await Muster durchgängig in der Python-Codebasis
- Cachen Sie häufig abgerufene Embeddings und Klassifizierungen
- Implementieren Sie Rate Limiting für externe API-Aufrufe