import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "DeepRead API"
    VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

    STORAGE_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "storage")

    # Uncomment for future use
    # REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "chroma_db")

settings = Settings()
