from fastapi import Request
from fastapi.exceptions import HTTPException

import os

from modules.scraper.validator import IngestRequest, IngestResponse
from modules.scraper.service import (
    scrape_and_save, 
    load_text,
    chunk_text,
    embed_and_store
)
from utils.config import settings

async def ingest_url(body: IngestRequest, request: Request) -> IngestResponse:
    data_file = os.path.join(settings.DATA_DIRECTORY, "data.md")
    result = await scrape_and_save(body.urls, data_file)

    if result["processed"] == 0:
        raise HTTPException(status_code=422, detail={"errors": result["errors"]})

    text = await load_text(data_file)
    chunks = await chunk_text(text, request.app.state.embedding_model)
    stored = await embed_and_store(chunks, request.app.state.collection, request.app.state.embedding_model)

    return IngestResponse(
        message="Ingest complete",
        chunks_stored=stored,
        urls_processed=result["processed"],
    )
