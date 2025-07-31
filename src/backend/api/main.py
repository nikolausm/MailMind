"""
MailMind FastAPI Application
Main entry point for the API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
# from .routes import emails, auth, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    print("Starting MailMind API...")
    # Initialize database connections
    # Initialize AI agents
    yield
    # Shutdown
    print("Shutting down MailMind API...")
    # Close database connections

app = FastAPI(
    title="MailMind API",
    description="Intelligent Email Client with RAG Implementation",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to MailMind API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
