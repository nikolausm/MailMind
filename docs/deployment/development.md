# Entwicklungsumgebung einrichten

## Inhaltsverzeichnis / Table of Contents

### In diesem Dokument
- [Voraussetzungen](#voraussetzungen)
- [Quick Start](#quick-start)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. Environment Setup](#3-environment-setup)
  - [4. Database Setup](#4-database-setup)
  - [5. Start Development Servers](#5-start-development-servers)
- [Development Tools](#development-tools)
  - [Code Quality](#code-quality)
  - [Testing](#testing)
  - [Database Management](#database-management)
- [IDE Setup](#ide-setup)
  - [VS Code](#vs-code)
  - [PyCharm/WebStorm](#pycharmwebstorm)
- [Debugging](#debugging)
  - [Backend Debugging](#backend-debugging)
  - [Frontend Debugging](#frontend-debugging)
- [Local Services](#local-services)
  - [Redis](#redis)
  - [PostgreSQL](#postgresql)
  - [Email Server (Development)](#email-server-development)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)

### Verwandte Dokumente
- [Docker-Konfiguration](./docker.md)
- [Produktiv-Deployment](./production.md)
- [REST API-Endpunkte](../api/endpoints.md)
- [API-Fehlercodes](../api/errors.md)

---

## Voraussetzungen
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Redis 6+

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/your-org/mailmind.git
cd mailmind
```

### 2. Install Dependencies
```bash
# Frontend
cd src/frontend
npm install

# Backend
cd ../..
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Database Setup
```bash
# Start PostgreSQL
createdb mailmind

# Run migrations
alembic upgrade head
```

### 5. Start Development Servers
```bash
# Terminal 1: Backend
npm run dev:backend

# Terminal 2: Frontend
npm run dev:frontend

# Or both:
npm run dev
```

## Development Tools

### Code Quality
```bash
# Python
black src/
flake8 src/
mypy src/

# Frontend
npm run lint
npm run type-check
```

### Testing
```bash
# Backend tests
pytest

# Frontend tests
npm test

# E2E tests
npm run test:e2e
```

### Database Management
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## IDE Setup

### VS Code
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

### PyCharm/WebStorm
- Configure Python interpreter with venv
- Enable TypeScript service
- Set up file watchers for formatting

## Debugging

### Backend Debugging
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use VS Code debugger with launch.json
```

### Frontend Debugging
- Use React Developer Tools
- Chrome DevTools for network inspection
- Redux DevTools for state management

## Local Services

### Redis
```bash
# Start Redis
redis-server

# Or with Docker
docker run -p 6379:6379 redis
```

### PostgreSQL
```bash
# Start PostgreSQL
pg_ctl start

# Or with Docker
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```

### Email Server (Development)
```bash
# Use MailHog for local email testing
docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :9000  # macOS/Linux
netstat -ano | findstr :9000  # Windows

# Kill process
kill -9 <PID>
```

#### Database Connection Error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check database exists

#### Modul-Import-Fehler
- Sicherstellen, dass virtuelle Umgebung aktiviert ist
- Abhängigkeiten neu installieren
- PYTHONPATH prüfen

#### Frontend-Build-Fehler
- node_modules löschen und neu installieren
- Node.js-Version prüfen
- Build-Cache leeren