---
title: "Magma RAG Service: Design & Implementation"
description: "Building a minimal RAG service for codebase indexing and semantic search"
publishDate: "28 July 2025"
theme: "@slidev/theme-default"
tags: ["rag", "machine-learning", "code-search", "llamaindex"]
draft: false
aspectRatio: "16:9"
---

## Magma RAG Service

### Design & Implementation Deep Dive

> Note: This project is closed source and no longer maintained.
> Inspiration: Based on rag-service from [avante.nvim](http://github.com/yetone/avante.nvim)

---

# 1. Introduction

- What is Magma?
- The Problem
- Our Solution

---

## What is Magma?

Minimal RAG service for codebase indexing and semantic search

- Natural Language → Code Search: Bridge queries and code with enhanced processing
- LlamaIndex + ChromaDB: Built on mature, proven technologies
- Specialized Pipeline: Code-aware processing and chunking
- Multi-Provider AI: Flexible AI integration with runtime switching

---

## The Problem

Traditional RAG struggles with code

### Raw Code
```python
# example kept small for slide readability

def authenticate_user(username, password):
    return verify_credentials(username, password)
```

### Poor Results
- ❌ Query: "How to implement authentication?"
- ❌ Poor semantic similarity between natural language and code
- ❌ Mixed results with random code fragments

### Enhanced Processing
- Context Extraction: Functions, classes, imports, keywords
- Domain Classification: auth, database, api, error handling
- Natural Language Description: Bridge language gap

---

## Our Solution: Dual Pipeline

- Standard Pipeline: Documents → Validation → Cleaning → Chunking → Embedding → ChromaDB
- Enhanced Pipeline: Code Files → Language Detection → Context Extraction → Natural Language Description → Enhanced Embedding → ChromaDB

---

# 2. System Architecture

- Core Design
- API Layer
- Service Layer
- Storage Strategy

---

## Core Architecture

### API Layer (FastAPI)
- RESTful endpoints
- OpenAPI documentation
- Health monitoring

### Service Layer
- Business logic
- Resource management
- Indexing orchestration

### Provider Layer
- Multi-AI support
- Factory pattern
- Runtime switching

### Storage Layer
- ChromaDB vectors
- SQLite metadata
- Dual strategy

---

## API Endpoints

| Method   | Endpoint                   | Purpose                  |
| :------- | :------------------------- | :----------------------- |
| **POST** | `/api/v1/add_resource`     | Resource management      |
| **POST** | `/api/v1/retrieve`         | Standard document search |
| **POST** | `/api/v1/code_retrieve`    | Enhanced code search     |
| **GET**  | `/api/v1/indexing_history` | Status monitoring        |
| **GET**  | `/health`                  | Health check             |

---

## Service Layer

- ResourceService: Manages indexed resources
- IndexingService: Orchestrates document processing
- CodeRetrievalService: Specialized code search
- IndexingHistoryService: Status tracking & monitoring

---

## Storage Strategy

### ChromaDB (Vector Store)
```python
self.chroma_client = chromadb.PersistentClient(
    path=str(settings.chroma_persist_dir)
)
vector_store = ChromaVectorStore(chroma_collection=collection)
```

### SQLite (Metadata)
- Resource Management: name, URI, status
- Indexing History: Status tracking
- Document Status: Individual monitoring
- Error Storage: Detailed error messages

---

# 3. Core Implementation

- Code Processing
- Multi-AI Provider System
- Performance & Monitoring

---

## Smart Code Processing

Language-Aware Chunking with Tree-sitter support for 15+ programming languages

### Code Splitter Configuration
```python
language = self.code_ext_map.get(file_ext, "python")
parser = get_parser(language)
code_splitter = CodeSplitter(
    language=language,
    chunk_lines=80,
    chunk_lines_overlap=15,
    max_chars=1500,
    parser=parser
)
```

---

## Context Extraction

### Enhanced Code Processing
```python
def _extract_code_context(self, code_content: str, language: str):
    context = {
        "functions": re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', code_content),
        "classes": re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', code_content),
        "imports": re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)', code_content),
        "keywords": self._extract_domain_keywords(code_content)
    }
```

Also, to bridge some of the semantic gaps with natural language, we use LLM to generate key descriptions for each snippet.

---

## Domain Classification

- auth: authentication, login, password, token
- database: query, select, insert, update, connection
- api: endpoint, route, request, response, handler
- error: exception, try, catch, handle

---

## Multi-AI Provider System

**Factory Pattern Implementation**: Runtime switching without code changes

### Provider Factory
```python
class ProviderFactory:
    def create_embedding_model(self, provider_name, model, **kwargs):
        provider_class = self._registry.get_provider_class(provider_name)
        provider = provider_class(config)
        return provider.create_embedding_model()
```

Supported Providers: OpenAI, Ollama, DashScope, OpenRouter

---

## Performance Optimizations

**Concurrent Processing with ThreadPoolExecutor**

### Batch Processing
```python
with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
    results = await loop.run_in_executor(
        executor,
        lambda: list(executor.map(
            lambda batch: self.document_processor.process_document_batch(
                batch, self.index
            ),
            batches
        ))
    )
```

Configurable: `document_batch_size`, `embed_batch_size`

---

## Real-Time File Monitoring

**Watchdog Integration**
```python
def start_watching_directory(self, directory: Path, uri: str):
    event_handler = FileSystemHandler(
        directory=directory,
        indexing_service=self
    )
    observer = Observer()
    observer.schedule(event_handler, str(directory), recursive=True)
    observer.start()
```

- Smart Filtering: Respects .gitignore patterns
- Binary Detection: Excludes encrypted files
- Debounced Changes: Efficient change detection

---

## Error Handling & Resilience

**Retry Logic with Exponential Backoff**

### Graceful Error Handling
```python
max_retries = 3
retry_count = 0
while retry_count < max_retries:
    try:
        index.refresh_ref_docs(valid_documents)
        break
    except Exception:
        retry_count += 1
        if retry_count < max_retries:
            time.sleep(2 ** retry_count)
```

---

# 4. Configuration & Deployment

- Environment Configuration
- Enhanced Code Retrieval
- Design Decisions

---

## Environment Configuration

**Runtime Configuration**: Switch providers without code changes

| Category        | Variable              | Options                                     |
| :-------------- | :-------------------- | :------------------------------------------ |
| **AI Provider** | `RAG_EMBED_PROVIDER`  | openai \| ollama \| dashscope \| openrouter |
| **AI Provider** | `RAG_LLM_PROVIDER`    | openai \| ollama \| dashscope \| openrouter |
| **Models**      | `RAG_EMBED_MODEL`     | text-embedding-3-small                      |
| **Models**      | `RAG_LLM_MODEL`       | gpt-4o-mini                                 |
| **Performance** | `DOCUMENT_BATCH_SIZE` | 10                                          |
| **Performance** | `EMBED_BATCH_SIZE`    | 100                                         |

---

## Enhanced Code Retrieval

### Query Classification
```python
code_keywords = [
    "implement", "function", "method", "code", "algorithm",
    "pattern", "syntax", "example", "struct", "enum", "fn"
]

if any(keyword in query.lower() for keyword in code_keywords):
    use_code_retrieve()
else:
    use_document_retrieve()
```

### Structured Response
```python
{
  "summary": "Found 3 error handling implementations...",
  "code_snippets": [
    {
      "uri": "file:///app/auth.rs",
      "content": "fn authenticate_user(...) -> Result",
      "language": "rust",
      "function_name": "authenticate_user",
      "score": 0.95
    }
  ]
}
```

---

## Design Decisions

### Why LlamaIndex?
- Mature ecosystem with extensive integrations
- Modular architecture allowing customization
- Built-in support for multiple vector stores
- Active development and community support

### Why ChromaDB?
- Embeddable vector database (no external dependencies)
- High performance with efficient indexing
- Simple API with Python-first design
- Persistent storage with automatic backups

### Why SQLite for Metadata?
- Zero configuration embedded database
- ACID transactions for data consistency
- Excellent Python support via SQLModel
- Reliable for metadata and small datasets

---

## Thank You!

Magma RAG Service: Design & Implementation

