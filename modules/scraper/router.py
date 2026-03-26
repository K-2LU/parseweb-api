from fastapi import APIRouter

scraper_router = APIRouter(prefix='/api/v1', tags=['parseweb'])

@router.get('/')
async def root():
    return {"message": "hello world"}