"""
Documentation API routes
Handles reading and writing markdown documentation files
"""

from fastapi import APIRouter, HTTPException, Body
from pathlib import Path
from typing import Dict, List, Optional
import os

router = APIRouter(prefix="/api/docs", tags=["documentation"])

# Base directory for documentation
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
DOCS_DIR = BASE_DIR / "docs"

def get_file_path(file_path: str) -> Path:
    """Resolve and validate file path"""
    # Remove leading slash if present
    file_path = file_path.lstrip("/")
    
    # Add .md extension if not present
    if not file_path.endswith('.md'):
        file_path = f"{file_path}.md"
    
    # Check if it's in docs directory or root
    if file_path.startswith("docs/"):
        full_path = BASE_DIR / file_path
    elif file_path in ["README.md", "CLAUDE.md", "CLAUDE_CODE_STATUS.md", "CLAUDE_CODE_INSTRUCTIONS.md"]:
        full_path = BASE_DIR / file_path
    else:
        # Try in docs directory first
        full_path = DOCS_DIR / file_path
        # If not found in docs, try root directory
        if not full_path.exists():
            root_path = BASE_DIR / file_path
            if root_path.exists():
                full_path = root_path
    
    # Security: ensure path doesn't escape base directory
    try:
        full_path = full_path.resolve()
        if not str(full_path).startswith(str(BASE_DIR)):
            raise ValueError("Invalid path")
    except:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    return full_path

@router.get("/")
async def list_documents() -> Dict[str, List[Dict[str, str]]]:
    """List all available documentation files"""
    documents = []
    
    # Add root level docs
    for file in ["README.md", "CLAUDE.md", "CLAUDE_CODE_STATUS.md"]:
        path = BASE_DIR / file
        if path.exists():
            documents.append({
                "path": file,
                "name": file,
                "category": "root"
            })
    
    # Add docs directory files
    if DOCS_DIR.exists():
        for file in DOCS_DIR.rglob("*.md"):
            rel_path = file.relative_to(BASE_DIR)
            documents.append({
                "path": str(rel_path),
                "name": file.name,
                "category": "docs"
            })
    
    return {"documents": documents}

@router.get("/{file_path:path}")
async def get_document(file_path: str) -> Dict[str, str]:
    """Get content of a specific document"""
    full_path = get_file_path(file_path)
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not full_path.is_file():
        raise HTTPException(status_code=400, detail="Path is not a file")
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {
            "path": file_path,
            "content": content,
            "exists": "true"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@router.put("/{file_path:path}")
async def update_document(
    file_path: str,
    content: str = Body(..., embed=True)
) -> Dict[str, str]:
    """Update or create a document"""
    full_path = get_file_path(file_path)
    
    # Create directory if it doesn't exist
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return {
            "path": file_path,
            "message": "Document saved successfully",
            "success": "true"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@router.delete("/{file_path:path}")
async def delete_document(file_path: str) -> Dict[str, str]:
    """Delete a document"""
    full_path = get_file_path(file_path)
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Don't allow deletion of core files
    protected_files = ["README.md", "CLAUDE.md", "CLAUDE_CODE_STATUS.md", 
                      "AUTHENTICATION.md", "AUTH_FLOWS.md"]
    if file_path in protected_files or full_path.name in protected_files:
        raise HTTPException(status_code=403, detail="Cannot delete protected file")
    
    try:
        full_path.unlink()
        return {
            "path": file_path,
            "message": "Document deleted successfully",
            "success": "true"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")