from pydantic import BaseModel

class IngestRequest(BaseModel):
    urls: list[str]


class IngestResponse(BaseModel):
    message: str
    chunks_stored: int
    urls_processed: int
