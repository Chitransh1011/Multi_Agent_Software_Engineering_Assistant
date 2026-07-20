from pydantic_settings import BaseSettings,SettingsConfigDict
import os
ENV_FILE = os.getenv("ENV_FILE", ".env")

class Settings(BaseSettings):
    openai_api_key:str
    gemini_key:str | None = None
    mem0_api_key:str | None = None
    NEO4J_URI:str | None = None
    NEO4J_USERNAME:str | None = None
    NEO4J_PASSWORD:str | None = None
    NEO4J_DATABASE:str | None = None
    AURA_INSTANCEID:str | None = None
    AURA_INSTANCENAME:str | None = None
    DATABASE_URL:str
    DEFAULT_MODEL : str = "gpt-4o-mini"
    MAX_RETRIES : int = 3
    RAG_DOCUMENT_PATH : str = "data/git_docs.pdf"

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

settings = Settings()