from fastapi import APIRouter, Request

from modules.scraper import controller
from modules.scraper.validator import IngestRequest

scraper_router = APIRouter(prefix='/parse/v1', tags=['parseweb'])

@scraper_router.get('/')
async def root():
    return {"message": "hello world"}

@scraper_router.post('/ingest')
async def ingest_url(body: IngestRequest, request: Request):
    return await controller.ingest_url(body, request)