from fastapi import APIRouter, Request

from modules.rag import controller
from modules.rag.validator import QueryRequest, QueryResponse

router = APIRouter(prefix="/rag/v1", tags=["rag"])

@router.get("/")
async def root():
    return {"message": "hello world"}

@router.post('/query')
async def query(body: QueryRequest, request: Request) -> QueryResponse:
    return await controller.query(body, request)