from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost/textbook_db"

    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    # API settings
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "Textbook Generation and RAG Chatbot API"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ADMIN_API_KEY: Optional[str] = None # New admin API key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LLM settings
    GROQ_API_KEY: Optional[str] = None
    LLM_MODEL: str = "llama3-8b-8192"  # Default model

    # Application settings
    DEBUG: bool = True
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes

    class Config:
        env_file = ".env"


# Create a settings instance
settings = Settings()