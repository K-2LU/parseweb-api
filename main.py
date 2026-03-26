# keep third party library imports here
from contextlib import asynccontextmanager
from fastapi import FastAPI

# python libraries here
import os

# local modules here
from modules.scraper.router import scraper_router
from utils.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.DATA_DIRECTORY, exist_ok=True)
    os.makedirs(settings.CHROMADB_DIRECTORY, exist_ok=True)

    print('loading embedding model...')
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(scraper_router)