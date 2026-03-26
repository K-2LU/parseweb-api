from pydantic_settings import (BaseSettings, SettingsConfigDict)

from .constants import (
    DEFAULT_GEMINI_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_COLLECTION_NAME
)

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DATA_DIRECTORY: str = './data'
    CHROMADB_DIRECTORY: str = './chroma_db'
    EMBEDDING_MODEL: str = DEFAULT_EMBEDDING_MODEL
    GEMINI_MODEL: str = DEFAULT_GEMINI_MODEL
    COLLECTION_NAME: str = DEFAULT_COLLECTION_NAME
    
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()