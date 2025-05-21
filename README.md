# llm_rag

graph TD
    A[Kafka Stream or Test Data] --> B[Embed with SentenceTransformer]
    B --> C[ChromaDB]
    A --> D[Query ChromaDB for Similar Items]
    D --> E[Build Prompt with Retrieved Docs]
    E --> F[Send to Ollama LLaMA]
    F --> G[Store Summary in PostgreSQL]
