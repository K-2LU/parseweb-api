from sentence_transformers import SentenceTransformer

import httpx
import aiofiles
from bs4 import BeautifulSoup

from utils.constants import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP

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

async def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
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