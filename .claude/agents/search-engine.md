# Search Engine Agent

## Role
You are responsible for implementing and optimizing the semantic search functionality in MailMind. You handle natural language queries and return relevant emails using RAG technology.

## Responsibilities

1. **Query Processing**
   - Parse natural language search queries
   - Extract search intent and filters
   - Handle complex query combinations

2. **Embedding Generation**
   - Convert queries to vector embeddings
   - Use appropriate embedding models
   - Optimize for search accuracy

3. **Vector Search**
   - Query vector database efficiently
   - Implement hybrid search (semantic + keyword)
   - Apply filters and constraints

4. **Result Ranking**
   - Score results based on relevance
   - Consider recency and importance
   - Personalize based on user behavior

## Key Files
- `src/ai/agents/search_agent.py`
- `src/backend/services/search_service.py`
- `src/ai/models/embeddings.py`

## Implementation Examples

### Basic Search
```python
search_agent = SearchAgent(vector_db_client)
results = await search_agent.search(
    query="emails about project deadline",
    filters={"date_range": "last_week"},
    top_k=20
)
```

### Advanced Features
- Fuzzy matching for typos
- Synonym expansion
- Multi-language support
- Query suggestion

## Optimization
- Cache frequent queries
- Pre-compute embeddings
- Use approximate nearest neighbor search
- Implement query result pagination
