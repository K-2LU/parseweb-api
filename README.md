# parseweb-api

A FastAPI backend that implements a RAG (Retrieval-Augmented Generation) pipeline. It scrapes website content, stores it as vector embeddings in ChromaDB, and answers natural-language questions against that content using Google Gemini.

## How it works

**Ingest:** URLs → scrape HTML → chunk text → embed (Sentence Transformers) → store in ChromaDB

**Query:** question → embed → retrieve top-k similar chunks → prompt Gemini with context → return answer

## Prerequisites

- Python >= 3.10
- [Poetry](https://python-poetry.org/docs/#installation)
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

## Setup

### 1. Clone and enter the project

```bash
git clone <repo-url>
cd parseweb-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install poetry
poetry install
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env   # if available, otherwise create manually
```

Add your API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Optional settings (shown with defaults):

```env
DATA_DIRECTORY=./data
CHROMADB_DIRECTORY=./chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
GENERATIVE_MODEL=gemini-2.5-flash
COLLECTION_NAME=markdown_docs
```

## Running the server

**Development (with hot-reload):**

```bash
poetry run dev
# or
uvicorn main:app --reload
```

**Production:**

```bash
uvicorn main:app
```

The API will be available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### Scraper

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/parse/v1/` | Health check |
| POST | `/parse/v1/ingest` | Scrape URLs and store embeddings |

**Ingest request:**

```json
{
  "urls": [
    "https://example.com/docs/page1",
    "https://example.com/docs/page2"
  ]
}
```

**Ingest response:**

```json
{
  "message": "Ingested 2 URLs, stored 34 chunks.",
  "chunks_stored": 34,
  "urls_processed": 2
}
```

### RAG

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rag/v1/` | Health check |
| POST | `/rag/v1/query` | Query ingested content |

**Query request:**

```json
{
  "question": "How does authentication work?",
  "top_k": 3
}
```

**Query response:**

```json
{
  "answer": "Authentication works by...",
  "chunks": ["chunk1 text", "chunk2 text", "chunk3 text"]
}
```

> Note: You must ingest at least one URL before querying.

## Project structure

```
parseweb-api/
├── main.py                  # App entry point, lifespan setup
├── pyproject.toml           # Dependencies and scripts
├── .env                     # Environment variables (not committed)
├── utils/
│   ├── config.py            # Pydantic settings
│   └── constants.py         # Default constants
└── modules/
    ├── scraper/
    │   ├── router.py        # /parse/v1/ routes
    │   ├── controller.py    # Ingest orchestration
    │   ├── service.py       # Scraping, chunking, embedding logic
    │   └── validator.py     # Request/response models
    └── rag/
        ├── router.py        # /rag/v1/ routes
        ├── controller.py    # Query orchestration
        ├── service.py       # Retrieval and generation logic
        └── validator.py     # Request/response models
```
