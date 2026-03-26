from fastapi import APIRouter

router = APIRouter(prefix="/rag/v1", tags=["rag"])

@router.get("/")
async def root():
    return {"message": "hello world"}