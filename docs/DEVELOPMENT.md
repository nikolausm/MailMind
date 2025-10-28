# MailMind Development Guide

## Inhaltsverzeichnis

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [AI Agents](#ai-agents)
- [Development with Claude Code](#development-with-claude-code)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## In diesem Dokument

- **[Quick Start](#quick-start)**: Schnelle Einrichtung des Entwicklungsumfelds
- **[Project Structure](#project-structure)**: Überblick über die Projektorganisation und Verzeichnisstruktur
- **[AI Agents](#ai-agents)**: Spezialisierte KI-Agenten und deren Funktionen
- **[Development with Claude Code](#development-with-claude-code)**: Richtlinien für die Entwicklung mit Claude Code
- **[Testing](#testing)**: Test-Strategien und Ausführung
- **[Deployment](#deployment)**: Anwendungsbereitstellung mit Docker
- **[Contributing](#contributing)**: Beitragsprozess und Richtlinien

## Verwandte Dokumente

- **[AI-Agenten](./ai-agents.md)**: Detaillierte AI-Agent-Spezifikationen und Architektur
- **[Agent-Architektur](./agent-architecture.md)**: Multi-Agent-System-Design
- **[Email-Pipeline](./email-pipeline.md)**: Email-Verarbeitungsprozesse
- **[Vektor-Datenbank](./vector-database.md)**: Embedding-Integration und semantische Suche
- **[Authentifizierung](./AUTHENTICATION.md)**: Entwicklungsaspekte der Authentifizierung
- **[Internationalisierung](./internationalization.md)**: i18n-Entwicklungsrichtlinien
- **[Dokumentations-Struktur](./DOCUMENTATION_STRUCTURE.md)**: Dokumentationsstandards

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/MailMind.git
   cd MailMind
   ```

2. **Install dependencies**
   ```bash
   npm install
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start development**
   ```bash
   npm run dev
   ```

## Project Structure

```
MailMind/
├── src/
│   ├── backend/         # Node.js/Python API server
│   │   ├── api/        # REST API endpoints
│   │   ├── services/   # Business logic
│   │   └── utils/      # Helper functions
│   ├── frontend/       # React web application
│   │   ├── components/ # UI components
│   │   ├── pages/     # Page components
│   │   └── hooks/     # Custom React hooks
│   ├── ai/            # AI/ML services
│   │   ├── agents/    # AI agents
│   │   ├── models/    # ML models
│   │   └── pipelines/ # Data processing
│   └── shared/        # Shared types and utilities
├── docs/              # Documentation
├── tests/             # Test suites
└── deployment/        # Docker and K8s configs
```

## AI Agents

The project includes several specialized AI agents:

1. **EmailClassifierAgent** (`src/ai/agents/email_classifier.py`)
   - Categorizes emails (work, personal, finance, etc.)
   - Assigns priority levels
   - Detects sentiment and urgency

2. **SearchAgent** (`src/ai/agents/search_agent.py`)
   - Handles semantic search queries
   - Manages vector embeddings
   - Integrates with vector database

3. **TaggingAgent** (`src/ai/agents/tagging_agent.py`)
   - Automatically generates tags
   - Creates hierarchical tag structures
   - Learns from user behavior

4. **SummaryAgent** (to be implemented)
   - Generates email thread summaries
   - Creates daily digests
   - Extracts action items

5. **ResponseAgent** (to be implemented)
   - Suggests intelligent replies
   - Adapts to writing style
   - Provides context-aware responses

## Development with Claude Code

When using Claude Code for development:

1. Focus on one agent at a time
2. Write comprehensive tests for each agent
3. Use type hints for all Python code
4. Follow the existing code structure
5. Document all API endpoints

## Testing

Run tests with:
```bash
# Python tests
pytest

# JavaScript tests
npm test
```

## Deployment

The application can be deployed using Docker:
```bash
docker build -t mailmind .
docker run -p 8000:8000 mailmind
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details
