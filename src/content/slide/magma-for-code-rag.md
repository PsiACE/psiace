---
title: "Magma RAG Service: Design & Implementation"
description: "Building a minimal RAG service for codebase indexing and semantic search"
publishDate: "28 July 2025"
theme: ["default", "/styles/breve-theme.css"]
tags: ["rag", "machine-learning", "code-search", "llamaindex"]
draft: false
---

<div class="title-slide">
<div class="main-title">Magma RAG Service</div>
<div class="subtitle">Design & Implementation Deep Dive</div>
</div>

> **Note**: This project is closed source and no longer maintained
>
> **Inspiration**: Based on rag-service from [avante.nvim](http://github.com/yetone/avante.nvim)

---

# 1. Introduction

<div class="section-outline">
<div class="outline-item">What is Magma?</div>
<div class="outline-item">The Problem</div>
<div class="outline-item">Our Solution</div>
</div>

---

## What is Magma?

<div class="insight-box">
<strong>Minimal RAG service for codebase indexing and semantic search</strong>
</div>

<div class="system-components">
<div class="component-card">
<h4>Natural Language → Code Search</h4>
<p>Bridge queries and code with enhanced processing</p>
</div>

<div class="component-card">
<h4>LlamaIndex + ChromaDB</h4>
<p>Built on mature, proven technologies</p>
</div>

<div class="component-card">
<h4>Specialized Pipeline</h4>
<p>Code-aware processing and chunking</p>
</div>

<div class="component-card">
<h4>Multi-Provider AI</h4>
<p>Flexible AI integration with runtime switching</p>
</div>
</div>

---

## The Problem

<div class="problem-statement">
<strong>Traditional RAG struggles with code</strong>
</div>

<div class="two-column">
<div class="column-left">

### Raw Code

```python
def authenticate_user(username, password):
    return verify_credentials(username, password)
```

### Poor Results

- ❌ **Query**: "How to implement authentication?"
- ❌ **Poor semantic similarity** between natural language and code
- ❌ **Mixed results** with random code fragments

</div>
<div class="column-right">

### Enhanced Processing

<div class="insight-card">
<h4>Context Extraction</h4>
<p>Functions, classes, imports, keywords</p>
</div>

<div class="insight-card">
<h4>Domain Classification</h4>
<p>auth, database, api, error handling</p>
</div>

<div class="insight-card">
<h4>Natural Language Description</h4>
<p>Bridge language gap</p>
</div>

</div>
</div>

---

## Our Solution: Dual Pipeline

<div class="strategy-grid">
<div class="strategy-card">
<h4>Standard Pipeline</h4>
<p>Documents → Validation → Cleaning → Chunking → Embedding → ChromaDB</p>
</div>

<div class="strategy-card">
<h4>Enhanced Pipeline</h4>
<p>Code Files → Language Detection → Context Extraction → Natural Language Description → Enhanced Embedding → ChromaDB</p>
</div>
</div>

---

# 2. System Architecture

<div class="section-outline">
<div class="outline-item">Core Design</div>
<div class="outline-item">API Layer</div>
<div class="outline-item">Service Layer</div>
<div class="outline-item">Storage Strategy</div>
</div>

---

## Core Architecture

<div class="level-details">
<div class="level-card">
<h4>API Layer (FastAPI)</h4>
<ul>
<li>RESTful endpoints</li>
<li>OpenAPI documentation</li>
<li>Health monitoring</li>
</ul>
</div>

<div class="level-card">
<h4>Service Layer</h4>
<ul>
<li>Business logic</li>
<li>Resource management</li>
<li>Indexing orchestration</li>
</ul>
</div>

<div class="level-card">
<h4>Provider Layer</h4>
<ul>
<li>Multi-AI support</li>
<li>Factory pattern</li>
<li>Runtime switching</li>
</ul>
</div>

<div class="level-card">
<h4>Storage Layer</h4>
<ul>
<li>ChromaDB vectors</li>
<li>SQLite metadata</li>
<li>Dual strategy</li>
</ul>
</div>
</div>

---

## API Endpoints

<div class="comparison-table">

| Method   | Endpoint                   | Purpose                  |
| :------- | :------------------------- | :----------------------- |
| **POST** | `/api/v1/add_resource`     | Resource management      |
| **POST** | `/api/v1/retrieve`         | Standard document search |
| **POST** | `/api/v1/code_retrieve`    | Enhanced code search     |
| **GET**  | `/api/v1/indexing_history` | Status monitoring        |
| **GET**  | `/health`                  | Health check             |

</div>

---

## Service Layer

<div class="system-components">
<div class="component-card">
<h4>ResourceService</h4>
<p>Manages indexed resources</p>
</div>

<div class="component-card">
<h4>IndexingService</h4>
<p>Orchestrates document processing</p>
</div>

<div class="component-card">
<h4>CodeRetrievalService</h4>
<p>Specialized code search</p>
</div>

<div class="component-card">
<h4>IndexingHistoryService</h4>
<p>Status tracking & monitoring</p>
</div>
</div>

---

## Storage Strategy

<div class="two-column">
<div class="column-left">

### ChromaDB (Vector Store)

<div class="formula-box">

```python
self.chroma_client = chromadb.PersistentClient(
    path=str(settings.chroma_persist_dir)
)
vector_store = ChromaVectorStore(chroma_collection=collection)
```

</div>

</div>
<div class="column-right">

### SQLite (Metadata)

<div class="insight-card">
<h4>Resource Management</h4>
<p>name, URI, status</p>
</div>

<div class="insight-card">
<h4>Indexing History</h4>
<p>Status tracking</p>
</div>

<div class="insight-card">
<h4>Document Status</h4>
<p>Individual monitoring</p>
</div>

<div class="insight-card">
<h4>Error Storage</h4>
<p>Detailed error messages</p>
</div>

</div>
</div>

---

# 3. Core Implementation

<div class="section-outline">
<div class="outline-item">Code Processing</div>
<div class="outline-item">Multi-AI Provider System</div>
<div class="outline-item">Performance & Monitoring</div>
</div>

---

## Smart Code Processing

<div class="insight-box">
<strong>Language-Aware Chunking with Tree-sitter support for 15+ programming languages</strong>
</div>

<div class="formula-box">
<strong>Code Splitter Configuration</strong>:

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

</div>

---

## Context Extraction

<div class="formula-box">
<strong>Enhanced Code Processing</strong>:

```python
def _extract_code_context(self, code_content: str, language: str):
    context = {
        "functions": re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', code_content),
        "classes": re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', code_content),
        "imports": re.findall(r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)', code_content),
        "keywords": self._extract_domain_keywords(code_content)
    }
```

Also, to bridge some of the semantic gaps with natural language, we use LLM to generate some key descriptions for each snippet.

</div>

---

## Domain Classification

<div class="insights-grid">
<div class="insight-card">
<h4>auth</h4>
<p>authentication, login, password, token</p>
</div>

<div class="insight-card">
<h4>database</h4>
<p>query, select, insert, update, connection</p>
</div>

<div class="insight-card">
<h4>api</h4>
<p>endpoint, route, request, response, handler</p>
</div>

<div class="insight-card">
<h4>error</h4>
<p>exception, try, catch, handle</p>
</div>
</div>

---

## Multi-AI Provider System

<div class="definition-box">
<strong>Factory Pattern Implementation</strong>: Runtime switching without code changes
</div>

<div class="formula-box">
<strong>Provider Factory</strong>:

```python
class ProviderFactory:
    def create_embedding_model(self, provider_name, model, **kwargs):
        provider_class = self._registry.get_provider_class(provider_name)
        provider = provider_class(config)
        return provider.create_embedding_model()
```

</div>

<div class="efficiency-note">
<strong>Supported Providers</strong>: OpenAI, Ollama, DashScope, OpenRouter
</div>

---

## Performance Optimizations

<div class="performance-summary">
<strong>Concurrent Processing with ThreadPoolExecutor</strong>
</div>

<div class="formula-box">
<strong>Batch Processing</strong>:

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

</div>

<div class="efficiency-note">
<strong>Configurable</strong>: `document_batch_size`, `embed_batch_size`
</div>

---

## Real-Time File Monitoring

<div class="formula-box">
<strong>Watchdog Integration</strong>:

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

</div>

<div class="insights-grid">
<div class="insight-card">
<h4>Smart Filtering</h4>
<p>Respects .gitignore patterns</p>
</div>

<div class="insight-card">
<h4>Binary Detection</h4>
<p>Excludes encrypted files</p>
</div>

<div class="insight-card">
<h4>Debounced Changes</h4>
<p>Efficient change detection</p>
</div>
</div>

---

## Error Handling & Resilience

<div class="problem-statement">
<strong>Retry Logic with Exponential Backoff</strong>
</div>

<div class="formula-box">
<strong>Graceful Error Handling</strong>:

```python
max_retries = 3
retry_count = 0
while retry_count < max_retries:
    try:
        index.refresh_ref_docs(valid_documents)
        break
    except Exception as e:
        retry_count += 1
        if retry_count < max_retries:
            time.sleep(2 ** retry_count)  # Exponential backoff
```

</div>

---

# 4. Configuration & Deployment

<div class="section-outline">
<div class="outline-item">Environment Configuration</div>
<div class="outline-item">Enhanced Code Retrieval</div>
<div class="outline-item">Design Decisions</div>
</div>

---

## Environment Configuration

<div class="definition-box">
<strong>Runtime Configuration</strong>: Switch providers without code changes
</div>

<div class="comparison-table">

| Category        | Variable              | Options                                     |
| :-------------- | :-------------------- | :------------------------------------------ |
| **AI Provider** | `RAG_EMBED_PROVIDER`  | openai \| ollama \| dashscope \| openrouter |
| **AI Provider** | `RAG_LLM_PROVIDER`    | openai \| ollama \| dashscope \| openrouter |
| **Models**      | `RAG_EMBED_MODEL`     | text-embedding-3-small                      |
| **Models**      | `RAG_LLM_MODEL`       | gpt-4o-mini                                 |
| **Performance** | `DOCUMENT_BATCH_SIZE` | 10                                          |
| **Performance** | `EMBED_BATCH_SIZE`    | 100                                         |

</div>

---

## Enhanced Code Retrieval

<div class="strategy-grid">
<div class="strategy-card">
<h4>Query Classification</h4>

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

</div>

<div class="strategy-card">
<h4>Structured Response</h4>

```python
{
  "summary": "Found 3 error handling implementations...",
  "code_snippets": [
    {
      "uri": "file:///app/auth.rs",
      "content": "fn authenticate_user(...) -> Result<User, AuthError>",
      "language": "rust",
      "function_name": "authenticate_user",
      "score": 0.95
    }
  ]
}
```

</div>
</div>

---

## Design Decisions

<div class="two-column">
<div class="column-left">

### Why LlamaIndex?

<div class="benefit-item">
<strong>Mature ecosystem</strong> with extensive integrations
</div>

<div class="benefit-item">
<strong>Modular architecture</strong> allowing customization
</div>

<div class="benefit-item">
<strong>Built-in support</strong> for multiple vector stores
</div>

<div class="benefit-item">
<strong>Active development</strong> and community support
</div>

</div>
<div class="column-right">

### Why ChromaDB?

<div class="benefit-item">
<strong>Embeddable</strong> vector database (no external dependencies)
</div>

<div class="benefit-item">
<strong>High performance</strong> with efficient indexing
</div>

<div class="benefit-item">
<strong>Simple API</strong> with Python-first design
</div>

<div class="benefit-item">
<strong>Persistent storage</strong> with automatic backups
</div>

</div>
</div>

### Why SQLite for Metadata?

<div class="benefit-item">
<strong>Zero configuration</strong> embedded database
</div>

<div class="benefit-item">
<strong>ACID transactions</strong> for data consistency
</div>

<div class="benefit-item">
<strong>Excellent Python support</strong> via SQLModel
</div>

<div class="benefit-item">
<strong>Reliable</strong> for metadata and small datasets
</div>

---

<div class="title-slide">
<div class="main-title">Thank You!</div>
<div class="subtitle">Magma RAG Service: Design & Implementation</div>
</div>
