# Backend-Architektur

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Übersicht](#übersicht)
- [Technologie-Stack](#technologie-stack)
- [Architektur-Schichten](#architektur-schichten)
- [Kern-Komponenten](#kern-komponenten)
- [API Endpoints](#api-endpoints)
- [Background Tasks](#background-tasks)
- [Security](#security)
- [Performance Optimizations](#performance-optimizations)
- [Monitoring & Observability](#monitoring--observability)
- [Deployment](#deployment)
- [Development Workflow](#development-workflow)
- [Future Enhancements](#future-enhancements)

### Verwandte Dokumente
- [🧠 KI-Agenten](./ai-agents.md) - Agent-System Dokumentation
- [🏛️ Agent-Architektur](./agent-architecture.md) - Agent-Design und Orchestrierung
- [📧 E-Mail-Pipeline](./email-pipeline.md) - E-Mail-Verarbeitungsfluss
- [🗂️ Vektor-Datenbank](./vector-database.md) - Embedding-Speicherung
- [📡 API Endpoints](./api/endpoints.md) - REST API Referenz

## Übersicht

MailMinds Backend ist mit einem modernen Python-Stack aufgebaut und fokussiert sich auf Performance, Skalierbarkeit und KI-Integration. Die Architektur folgt Microservice-Prinzipien und behält dabei die Einfachheit für die Entwicklung bei.

## Technologie-Stack

### Kern-Framework
- **FastAPI**: Hochperformantes asynchrones Web-Framework
- **Python 3.11+**: Neueste Python-Features für Type Hints und Async-Unterstützung
- **Pydantic**: Datenvalidierung und Einstellungsverwaltung
- **SQLAlchemy**: ORM für Datenbankoperationen

### KI & ML Stack
- **LangChain**: RAG-Implementierung und Agenten-Orchestrierung
- **OpenAI/Anthropic APIs**: LLM-Anbieter für intelligente Features
- **Sentence Transformers**: Lokale Embedding-Generierung
- **Vektor-Datenbank**: Pinecone/Weaviate für semantische Suche

## Architektur-Schichten

```
┌─────────────────────────────────────────────┐
│            API Gateway (FastAPI)            │
├─────────────────────────────────────────────┤
│            Service Layer                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  Email   │ │    AI    │ │  Search  │   │
│  │ Service  │ │ Service  │ │ Service  │   │
│  └──────────┘ └──────────┘ └──────────┘   │
├─────────────────────────────────────────────┤
│            Agent Orchestration              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │Classifier│ │ Tagging  │ │ Summary  │   │
│  │  Agent   │ │  Agent   │ │  Agent   │   │
│  └──────────┘ └──────────┘ └──────────┘   │
├─────────────────────────────────────────────┤
│           Data Access Layer                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │PostgreSQL│ │  Redis   │ │ Vector DB│   │
│  └──────────┘ └──────────┘ └──────────┘   │
└─────────────────────────────────────────────┘
```

## Kern-Komponenten

### 1. API Gateway (`src/backend/api/`)

Das API Gateway behandelt alle eingehenden HTTP-Anfragen und WebSocket-Verbindungen.

```python
# main.py
app = FastAPI(
    title="MailMind API",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware stack
app.add_middleware(CORSMiddleware, ...)
app.add_middleware(AuthenticationMiddleware, ...)
app.add_middleware(RateLimitMiddleware, ...)
```

**Hauptfunktionen:**
- RESTful API-Endpunkte
- WebSocket-Unterstützung für Echtzeit-Updates
- OpenAPI-Dokumentation
- Anfrage-Validierung
- Fehlerbehandlung

### 2. Service-Schicht (`src/backend/services/`)

Ge-schäftslogik ist in Service-Klassen eingekapselt:

#### E-Mail-Service
```python
class EmailService:
    async def fetch_emails(self, account_id: str) -> List[Email]:
        """E-Mails vom IMAP-Server abrufen"""
        
    async def send_email(self, email: EmailCreate) -> Email:
        """E-Mail via SMTP senden"""
        
    async def sync_emails(self, account_id: str) -> SyncResult:
        """E-Mails mit Remote-Server synchronisieren"""
```

#### KI-Service
```python
class AIService:
    async def classify_email(self, email: Email) -> Classification:
        """E-Mail mit KI klassifizieren"""
        
    async def generate_tags(self, email: Email) -> List[Tag]:
        """Hierarchische Tags generieren"""
        
    async def summarize_thread(self, thread: EmailThread) -> str:
        """Thread-Zusammenfassung erstellen"""
```

### 3. Agenten-System (`src/ai/`)

Das KI-Agenten-System nutzt ein Orchestrator-Pattern für koordinierte Verarbeitung:

```python
class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            'classifier': EmailClassifierAgent(),
            'tagger': TaggingAgent(),
            'search': SearchAgent(),
            'summary': SummaryAgent()
        }
    
    async def process_email(self, email: Email) -> ProcessingResult:
        """E-Mail durch Agenten-Pipeline verarbeiten"""
        tasks = [
            self.agents['classifier'].process(email),
            self.agents['tagger'].process(email),
            self._generate_embeddings(email)
        ]
        results = await asyncio.gather(*tasks)
        return self._consolidate_results(results)
```

### 4. Datenmodelle (`src/backend/models/`)

#### Datenbank-Modelle (SQLAlchemy)
```python
class EmailModel(Base):
    __tablename__ = "emails"
    
    id = Column(UUID, primary_key=True)
    message_id = Column(String, unique=True)
    subject = Column(String)
    body = Column(Text)
    sender = Column(String)
    recipients = Column(JSON)
    timestamp = Column(DateTime)
    
    # KI-generierte Felder
    classification = Column(String)
    importance_score = Column(Float)
    tags = relationship("Tag", back_populates="email")
    embedding_id = Column(String)  # Referenz zur Vektor-DB
```

#### API-Modelle (Pydantic)
```python
class EmailResponse(BaseModel):
    id: str
    subject: str
    body: str
    sender: str
    recipients: List[str]
    timestamp: datetime
    classification: Optional[str]
    tags: List[str]
    summary: Optional[str]
```

### 5. Datenbank-Schicht

#### PostgreSQL (Haupt-Datenbank)
- Benutzerkonten und Authentifizierung
- E-Mail-Metadaten und -Inhalte
- Tags und Klassifizierungen
- System-Konfiguration

#### Redis (Cache & Queue)
- Session-Management
- API-Response-Caching
- Task-Queue für Hintergrund-Jobs
- Echtzeit-Benachrichtigungen Pub/Sub

#### Vektor-Datenbank (Semantische Suche)
- E-Mail-Embeddings
- Ähnlichkeitssuche-Indizes
- Clustering-Daten
- Anfrage-Embeddings

## API Endpoints

### Authentication
```
POST   /api/auth/login          # Login with credentials
POST   /api/auth/logout         # Logout current session
POST   /api/auth/refresh        # Refresh access token
POST   /api/auth/register       # Register new account
```

### Email Management
```
GET    /api/emails              # List emails with pagination
GET    /api/emails/{id}         # Get specific email
POST   /api/emails              # Send new email
PUT    /api/emails/{id}         # Update email (draft)
DELETE /api/emails/{id}         # Delete email
POST   /api/emails/{id}/reply   # Reply to email
POST   /api/emails/{id}/forward # Forward email
```

### Search & AI
```
GET    /api/search              # Semantic search
POST   /api/ai/classify         # Classify emails
POST   /api/ai/generate-tags    # Generate tags
POST   /api/ai/summarize        # Summarize thread
GET    /api/ai/suggestions      # Get AI suggestions
```

### Account Management
```
GET    /api/accounts            # List email accounts
POST   /api/accounts            # Add email account
PUT    /api/accounts/{id}       # Update account
DELETE /api/accounts/{id}       # Remove account
POST   /api/accounts/{id}/sync  # Trigger sync
```

## Background Tasks

### Email Synchronization
```python
@celery.task
async def sync_email_account(account_id: str):
    """Periodic email synchronization"""
    service = EmailService()
    result = await service.sync_emails(account_id)
    
    # Process new emails through AI pipeline
    for email in result.new_emails:
        await process_email_with_ai.delay(email.id)
```

### AI Processing Pipeline
```python
@celery.task
async def process_email_with_ai(email_id: str):
    """Process email through AI agents"""
    email = await get_email(email_id)
    orchestrator = AgentOrchestrator()
    result = await orchestrator.process_email(email)
    await save_processing_results(email_id, result)
```

## Security

### Authentication & Authorization
- JWT tokens with refresh mechanism
- OAuth2 support for external providers
- Role-based access control (RBAC)
- API key authentication for programmatic access

### Data Protection
- Encryption at rest for sensitive data
- TLS/SSL for all communications
- Email content encryption options
- Secure credential storage (OAuth tokens, passwords)

### Rate Limiting
```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_id(request)
    if not rate_limiter.allow_request(client_id):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"}
        )
    return await call_next(request)
```

## Performance Optimizations

### Async/Await Pattern
All I/O operations use async/await for maximum concurrency:
```python
async def fetch_and_process_emails(account_id: str):
    # Concurrent fetching
    emails = await email_service.fetch_emails(account_id)
    
    # Parallel processing
    tasks = [process_email(email) for email in emails]
    results = await asyncio.gather(*tasks)
    
    return results
```

### Caching Strategy
- Redis for frequently accessed data
- In-memory caching for hot paths
- CDN for static assets
- Query result caching with TTL

### Database Optimization
- Connection pooling
- Query optimization with indexes
- Lazy loading for relationships
- Batch operations for bulk updates

## Monitoring & Observability

### Logging
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "email_processed",
    email_id=email.id,
    processing_time=elapsed,
    agent_results=results
)
```

### Metrics
- Prometheus metrics for performance monitoring
- Custom metrics for AI agent performance
- Email processing pipeline metrics
- API endpoint latency tracking

### Health Checks
```python
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "vector_db": await check_vector_db(),
        "ai_service": await check_ai_service()
    }
    
    status = "healthy" if all(checks.values()) else "unhealthy"
    return {"status": status, "checks": checks}
```

## Deployment

### Docker Configuration
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
```

### Environment Configuration
```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
```

### Scaling Considerations
- Horizontal scaling with load balancer
- Database read replicas
- Redis clustering
- Vector database sharding
- CDN for static content

## Development Workflow

### Local Development
```bash
# Start with hot reload
uvicorn main:app --reload --port 9000

# Run tests
pytest tests/ --cov=src

# Type checking
mypy src/

# Linting
black src/
flake8 src/
```

### Testing Strategy
- Unit tests for services and agents
- Integration tests for API endpoints
- End-to-end tests for critical workflows
- Performance testing for AI operations

## Future Enhancements

- GraphQL API support
- gRPC for internal services
- Event sourcing for audit trail
- Multi-tenant architecture
- Kubernetes deployment
- Advanced caching with Redis Streams
- Real-time collaboration features