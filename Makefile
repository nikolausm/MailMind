.PHONY: help setup start stop clean init-db generate-data classify-emails test

help:
	@echo "MailMind Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Install all dependencies"
	@echo "  make init-db        - Initialize database and load sample data"
	@echo ""
	@echo "Development:"
	@echo "  make start          - Start all services (DB + API + Frontend)"
	@echo "  make start-db       - Start databases only (PostgreSQL + Weaviate)"
	@echo "  make start-api      - Start backend API server"
	@echo "  make start-frontend - Start frontend dev server"
	@echo "  make stop           - Stop all services"
	@echo ""
	@echo "Data:"
	@echo "  make generate-data  - Generate sample email dataset"
	@echo "  make classify-emails - Classify unclassified emails"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean up generated files"

setup:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "📦 Installing Node.js dependencies..."
	cd src/frontend && npm install
	@echo "✅ Setup complete!"

start-db:
	@echo "🚀 Starting databases..."
	docker-compose up -d postgres weaviate
	@echo "⏳ Waiting for databases to be ready..."
	sleep 5
	@echo "✅ Databases started!"

start-api:
	@echo "🚀 Starting API server..."
	cd src/backend/api && uvicorn main:app --reload --port 8000

start-frontend:
	@echo "🚀 Starting frontend..."
	cd src/frontend && npm run dev

start: start-db
	@echo "🚀 Starting all services..."
	@echo "💡 Open terminals for:"
	@echo "   Terminal 1: make start-api"
	@echo "   Terminal 2: make start-frontend"

stop:
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ Services stopped!"

generate-data:
	@echo "📧 Generating sample emails..."
	python scripts/generate_sample_emails.py
	@echo "✅ Sample data generated!"

init-db: start-db
	@echo "🗄️  Initializing database..."
	sleep 3
	python scripts/init_database.py
	@echo "✅ Database initialized!"

classify-emails:
	@echo "🤖 Classifying emails..."
	curl -X POST "http://localhost:8000/emails/batch-classify?limit=50"
	@echo ""
	@echo "✅ Classification complete!"

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v
	@echo "✅ Tests complete!"

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf data/*.json
	@echo "✅ Cleanup complete!"
