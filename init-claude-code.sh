#!/bin/bash

# Claude Code Initialization Script for MailMind

echo "🚀 Initializing MailMind for Claude Code development..."

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d ".claude" ]; then
    echo "❌ Error: Please run this script from the MailMind project root"
    exit 1
fi

echo "📦 Installing dependencies..."

# Install Python dependencies
if command -v python3 &> /dev/null; then
    echo "Setting up Python environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "⚠️  Python 3 not found. Please install Python 3.9+"
fi

# Install Node dependencies
if command -v npm &> /dev/null; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "⚠️  npm not found. Please install Node.js 18+"
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p src/backend/{api/routes,services,models,database}
mkdir -p src/frontend/{components,pages,hooks,utils}
mkdir -p src/ai/{models,pipelines,utils}
mkdir -p tests/{unit,integration,e2e}

# Set up environment file
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys"
fi

echo "✅ MailMind initialization complete!"
echo ""
echo "📝 Claude Code Agents available:"
echo "  - email-processor: Email processing and classification"
echo "  - search-engine: Semantic search implementation"
echo "  - api-developer: REST API development"
echo "  - frontend-developer: React UI development"
echo "  - database-architect: Database schema and optimization"
echo ""
echo "🎯 Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Start development: npm run dev"
echo "  3. Run tests: npm test && pytest"
echo ""
echo "📚 Documentation:"
echo "  - Project overview: README.md"
echo "  - Development guide: docs/DEVELOPMENT.md"
echo "  - Agent details: .claude/agents/"
