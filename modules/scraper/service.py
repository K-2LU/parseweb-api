from sentence_transformers import SentenceTransformer

import re
import httpx
import aiofiles
import numpy as np
from bs4 import BeautifulSoup

from utils.constants import DEFAULT_SEMANTIC_THRESHOLD

async def scrape_and_save(urls: list[str], filepath: str) -> dict:
    """Scrape each URL and overwrite filepath with combined content."""
    # Overwrite file on each ingest to avoid duplicate chunks
    async with aiofiles.open(filepath, "w"):
        pass

    processed = 0
    errors = {}

    async with httpx.AsyncClient(timeout=15, verify=False) as client:
        for url in urls:
            try:
                response = await client.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                async with aiofiles.open(filepath, "a", encoding="utf-8") as f:
                    await f.write(text)
                processed += 1
            except Exception as e:
                errors[url] = str(e)

    return {"processed": processed, "errors": errors}

async def load_text(path: str) -> str:
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        text = await f.read()
        return text.strip()

def _split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

async def chunk_text(
    text: str,
    embedding_model: SentenceTransformer,
    breakpoint_threshold: float = DEFAULT_SEMANTIC_THRESHOLD,
) -> list[str]:
    sentences = _split_sentences(text)
    if not sentences:
        return []

    embeddings = embedding_model.encode(sentences, show_progress_bar=False)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / np.where(norms == 0, 1, norms)

    chunks = []
    current: list[str] = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = float(np.dot(normalized[i - 1], normalized[i]))
        if similarity < breakpoint_threshold:
            chunks.append(" ".join(current))
            current = [sentences[i]]
        else:
            current.append(sentences[i])

    if current:
        chunks.append(" ".join(current))

    return chunks

async def embed_and_store(chunks: list[str], collection, embedding_model: SentenceTransformer) -> int:
    """Clear collection and store new chunks."""
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    embeddings = embedding_model.encode(chunks, show_progress_bar=False).tolist()
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk-{i}" for i in range(len(chunks))],
    )
    return len(chunks)