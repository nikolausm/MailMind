# MailMind - Quick Setup Guide

## Prerequisites

- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **Docker and Docker Compose** installed
- **OpenAI API key** (or Anthropic API key)

## Quick Start (5 minutes)

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/nikolausm/MailMind.git
cd MailMind

# Copy environment file
cp .env.example .env

# Edit .env and add your API key
# Minimum required: OPENAI_API_KEY or ANTHROPIC_API_KEY
nano .env  # or your favorite editor
```

### 2. Install Dependencies

```bash
# Install all dependencies (Python + Node.js)
make setup

# Or manually:
pip install -r requirements.txt
cd src/frontend && npm install && cd ../..
```

### 3. Start Databases

```bash
# Start PostgreSQL and Weaviate
make start-db

# Wait ~10 seconds for databases to be ready
```

### 4. Initialize Database with Sample Data

```bash
# Generate sample emails
make generate-data

# Initialize database and load sample emails
make init-db
```

### 5. Start Backend API (Terminal 1)

```bash
make start-api

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 6. Classify Emails with AI (Terminal 2, while API is running)

```bash
# Classify the first 50 emails
make classify-emails

# Or use the API directly:
curl -X POST "http://localhost:8000/emails/batch-classify?limit=50"
```

### 7. Start Frontend (Terminal 3)

```bash
make start-frontend

# Frontend will be available at http://localhost:9000
```

## Testing the System

### Test API Endpoints

```bash
# Get email list
curl http://localhost:8000/emails/

# Get statistics
curl http://localhost:8000/emails/stats/overview

# Search emails
curl -X POST http://localhost:8000/emails/search \
  -H "Content-Type: application/json" \
  -d '{"query": "urgent meeting", "limit": 10}'
```

### Test Frontend

Open your browser to http://localhost:9000 and you should see the MailMind interface.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         MailMind                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (React)                                           │
│  └─ http://localhost:9000                                   │
│                                                             │
│  Backend API (FastAPI)                                      │
│  └─ http://localhost:8000                                   │
│     ├─ /emails          - Email CRUD                        │
│     ├─ /emails/search   - Semantic search                   │
│     └─ /emails/classify - AI classification                 │
│                                                             │
│  Databases (Docker)                                         │
│  ├─ PostgreSQL:5432     - Email storage                     │
│  └─ Weaviate:8080       - Vector embeddings                 │
│                                                             │
│  AI Agents                                                  │
│  ├─ EmailClassifierAgent - Category/Priority/Tags          │
│  └─ SearchAgent         - Semantic search with RAG          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Development Workflow

### Daily Development

```bash
# Terminal 1: Start databases (run once)
make start-db

# Terminal 2: Start API (auto-reloads on code changes)
make start-api

# Terminal 3: Start frontend (auto-reloads)
make start-frontend
```

### Adding New Emails

```bash
# Generate more sample emails
python scripts/generate_sample_emails.py

# Load into database
python scripts/init_database.py

# Classify new emails
make classify-emails
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/unit/test_email_classifier.py -v
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if databases are running
docker-compose ps

# Check database logs
docker-compose logs postgres
docker-compose logs weaviate

# Restart databases
make stop
make start-db
```

### API Won't Start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Make sure you're in the correct directory
cd src/backend/api
uvicorn main:app --reload --port 8000
```

### Frontend Issues

```bash
# Clear node modules and reinstall
cd src/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "No API Key" Errors

Make sure your `.env` file has a valid API key:

```bash
# For OpenAI
OPENAI_API_KEY=sk-...your-key-here...

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
LLM_PROVIDER=anthropic
```

## Project Structure

```
MailMind/
├── src/
│   ├── ai/                     # AI agents
│   │   ├── agents/
│   │   │   ├── email_classifier.py  # Classification agent
│   │   │   └── search_agent.py      # Search agent
│   │   └── orchestrator.py     # Agent coordinator
│   ├── backend/
│   │   ├── api/                # FastAPI application
│   │   │   ├── main.py         # API entry point
│   │   │   └── routes/         # API endpoints
│   │   ├── database/           # Database models
│   │   │   ├── models.py       # SQLAlchemy models
│   │   │   └── schemas.py      # Pydantic schemas
│   │   └── vector_db.py        # Weaviate client
│   └── frontend/               # React application
├── scripts/
│   ├── generate_sample_emails.py   # Generate test data
│   └── init_database.py            # Database initialization
├── data/                       # Generated data
├── tests/                      # Test suites
├── docker-compose.yml          # Database services
├── requirements.txt            # Python dependencies
└── Makefile                    # Development commands
```

## Next Steps

1. **Customize the UI**: Edit `src/frontend/src/`
2. **Add more agents**: Create new agents in `src/ai/agents/`
3. **Connect IMAP**: Implement email fetching
4. **Add authentication**: Implement user login
5. **Deploy**: See `docs/deployment/` for deployment guides

## Getting Help

- **Documentation**: See `docs/` directory
- **API Docs**: http://localhost:8000/docs (when API is running)
- **Issues**: https://github.com/nikolausm/MailMind/issues

Happy coding! 🚀
