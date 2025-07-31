# Claude Code Configuration for MailMind

## Project Overview
MailMind is an intelligent email client that uses RAG (Retrieval-Augmented Generation) to provide semantic search, auto-tagging, and AI-powered insights.

## Development Guidelines

### Architecture
- Backend: Node.js/Python API server
- Frontend: React-based web application
- AI/ML: Python-based services with LLM integration
- Database: PostgreSQL for metadata, Vector DB for embeddings

### Code Standards
- TypeScript for frontend
- Python 3.9+ for AI services
- ESLint and Black for code formatting
- Jest for testing

### AI Agents Structure
Located in `src/ai/agents/`:
1. **EmailClassifierAgent**: Categorizes and prioritizes emails
2. **SearchAgent**: Handles semantic search
3. **TaggingAgent**: Auto-tagging functionality
4. **SummaryAgent**: Thread summarization
5. **ResponseAgent**: Smart reply suggestions

### Development Workflow
1. Feature branches from main
2. PR-based development
3. AI agents tested with unit tests
4. Integration tests for API endpoints

### Environment Setup
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Key Technologies
- Vector Database: Weaviate/Pinecone
- LLM: OpenAI/Anthropic API
- Email: IMAP/Gmail API integration
- Search: Semantic embeddings with sentence-transformers
