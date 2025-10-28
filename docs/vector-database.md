# Vektor-Datenbank-Integration

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Unterstützte Vektor-Datenbanken](#unterstützte-vektor-datenbanken)
  - [Pinecone](#pinecone)
  - [Weaviate](#weaviate)
- [Embedding-Generierung](#embedding-generierung)
  - [Modell-Auswahl](#modell-auswahl)
  - [Embedding-Pipeline](#embedding-pipeline)
- [Vektor-Operationen](#vektor-operationen)
  - [Indizierung](#indizierung)
  - [Ähnlichkeitssuche](#ähnlichkeitssuche)
  - [Hybrid-Suche](#hybrid-suche)
- [Performance-Optimierung](#performance-optimierung)
  - [Batch-Verarbeitung](#batch-verarbeitung)
  - [Caching](#caching)
- [Index-Verwaltung](#index-verwaltung)
  - [Schema-Definition](#schema-definition)
  - [Index-Metriken](#index-metriken)

## In diesem Dokument

- **[Übersicht](#übersicht)**: Einführung in die Vektor-Datenbank-Integration
- **[Unterstützte Datenbanken](#unterstützte-vektor-datenbanken)**: Pinecone und Weaviate Setup
- **[Embedding-Generierung](#embedding-generierung)**: Modell-Auswahl und Pipeline
- **[Vektor-Operationen](#vektor-operationen)**: Indizierung und Suche
- **[Performance-Optimierung](#performance-optimierung)**: Batch-Verarbeitung und Caching
- **[Index-Verwaltung](#index-verwaltung)**: Schema und Metriken

## Verwandte Dokumente

- **[KI-Agenten](./ai-agents.md)**: SearchAgent-Implementierung
- **[E-Mail-Pipeline](./email-pipeline.md)**: Integration in die Verarbeitungspipeline
- **[AI-Interaktions-Regeln](./ai-interaction-rules.md)**: Such-Regeln und -Logik
- **[Agent-Architektur](./agent-architecture.md)**: Architektureller Kontext
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien

## Übersicht

Semantische Suchimplementierung mit Vektor-Embeddings für intelligenten E-Mail-Abruf.

## Unterstützte Vektor-Datenbanken

### Pinecone
```python
import pinecone

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment="us-west1-gcp"
)

index = pinecone.Index("mailmind-emails")
```

### Weaviate
```python
import weaviate

client = weaviate.Client(
    url="http://localhost:8080",
    auth_client_secret=weaviate.AuthApiKey(api_key="...")
)
```

## Embedding-Generierung

### Modell-Auswahl
```python
from sentence_transformers import SentenceTransformer

# Modelle nach Anwendungsfall
models = {
    "general": "all-MiniLM-L6-v2",          # Schnell, allgemein
    "multilingual": "paraphrase-multilingual-MiniLM-L12-v2",
    "large": "all-mpnet-base-v2",           # Höhere Qualität
    "domain": "custom-email-model"          # Feinabgestimmt
}

embedder = SentenceTransformer(models["general"])
```

### Embedding-Pipeline
```python
def generate_embedding(email: Email) -> np.ndarray:
    # Relevante Felder kombinieren
    text = f"{email.subject} {email.body}"
    
    # Embedding generieren
    embedding = embedder.encode(text)
    
    # Normalisieren
    embedding = embedding / np.linalg.norm(embedding)
    
    return embedding
```

## Vektor-Operationen

### Indizierung
```python
async def index_email(email: Email):
    # Embedding generieren
    embedding = generate_embedding(email)
    
    # Metadaten vorbereiten
    metadata = {
        "email_id": email.id,
        "subject": email.subject,
        "sender": email.sender,
        "date": email.timestamp.isoformat(),
        "tags": email.tags
    }
    
    # In Vektor-DB einfügen
    index.upsert(
        vectors=[(email.id, embedding.tolist(), metadata)]
    )
```

### Ähnlichkeitssuche
```python
async def semantic_search(query: str, top_k: int = 10):
    # Anfrage-Embedding generieren
    query_embedding = embedder.encode(query)
    
    # Suchen
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )
    
    return results
```

### Hybrid-Suche
```python
def hybrid_search(query: str, filters: dict = None):
    # Semantische Suche
    semantic_results = semantic_search(query)
    
    # Schlüsselwort-Suche
    keyword_results = keyword_search(query)
    
    # Kombinieren und neu bewerten
    combined = merge_results(semantic_results, keyword_results)
    return rerank_results(combined, query)
```

## Performance-Optimierung

### Batch-Verarbeitung
```python
async def batch_index_emails(emails: List[Email]):
    # Embeddings in Batches generieren
    texts = [f"{e.subject} {e.body}" for e in emails]
    embeddings = embedder.encode(texts, batch_size=32)
    
    # Batch-Upsert vorbereiten
    vectors = [
        (email.id, emb.tolist(), get_metadata(email))
        for email, emb in zip(emails, embeddings)
    ]
    
    # In Chunks einfügen
    for chunk in chunks(vectors, 100):
        index.upsert(vectors=chunk)
```

### Caching
```python
@lru_cache(maxsize=1000)
def get_cached_embedding(text_hash: str):
    return embeddings_cache.get(text_hash)
```

## Index-Verwaltung

### Schema-Definition
```json
{
  "name": "Email",
  "vectorizer": "text2vec-transformers",
  "properties": [
    {
      "name": "content",
      "dataType": ["text"],
      "indexFilterable": true,
      "indexSearchable": true
    },
    {
      "name": "subject",
      "dataType": ["string"],
      "indexFilterable": true
    },
    {
      "name": "sender",
      "dataType": ["string"],
      "indexFilterable": true
    },
    {
      "name": "timestamp",
      "dataType": ["date"],
      "indexFilterable": true
    }
  ]
}
```

### Index-Metriken
- **Dimension**: 384 (für all-MiniLM-L6-v2)
- **Metrik**: Kosinus-Ähnlichkeit
- **Index-Typ**: HNSW (Hierarchical Navigable Small World)
- **Replikas**: 2 für hohe Verfügbarkeit