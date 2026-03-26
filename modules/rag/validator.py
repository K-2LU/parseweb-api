from typing import List
from pydantic import BaseModel
from utils.constants import DEFAULT_TOP_K

class QueryRequest(BaseModel):
    question: str
    top_k: int = DEFAULT_TOP_K

class QueryResponse(BaseModel):
    answer: str
    chunks: List[str]