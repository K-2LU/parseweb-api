# keep third party library imports here
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

# python libraries here
import os

# local modules here
from modules.scraper.router import scraper_router
from modules.rag.router import router as rag_router
from utils.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.DATA_DIRECTORY, exist_ok=True)
    os.makedirs(settings.CHROMADB_DIRECTORY, exist_ok=True)

    print("Loading embedding model...")
    app.state.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

    chroma_client = chromadb.PersistentClient(path=settings.CHROMADB_DIRECTORY)
    app.state.collection = chroma_client.get_or_create_collection(name=settings.COLLECTION_NAME)

    genai.configure(api_key=settings.GEMINI_API_KEY)
    app.state.generative_model = genai.GenerativeModel(settings.GENERATIVE_MODEL)

    app.state.settings = settings

    print("Startup complete.")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(scraper_router)
app.include_router(rag_router)