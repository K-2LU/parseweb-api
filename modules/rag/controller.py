from fastapi import Request, HTTPException

from modules.rag.validator import QueryRequest, QueryResponse
from modules.rag import service

async def query(body: QueryRequest, request: Request) -> QueryResponse:
    if request.app.state.collection.count() == 0:
        raise HTTPException(status_code=404, detail="No data ingested yet")
    
    # ask service
    answer, chunks = await service.query(
        query=body.question,
        top_k=body.top_k,
        collection=request.app.state.collection,
        embedding_model=request.app.state.embedding_model,
        generative_model=request.app.state.generative_model
    )
    
    return QueryResponse(
        answer=answer,
        chunks=chunks
    )