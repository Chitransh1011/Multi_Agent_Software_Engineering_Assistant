from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key:str
    gemini_key:str
    mem0_api_key:str
    NEO4J_URI:str
    NEO4J_USERNAME:str
    NEO4J_PASSWORD:str
    NEO4J_DATABASE:str
    AURA_INSTANCEID:str
    AURA_INSTANCENAME:str
    DATABASE_URL:str
    DEFAULT_MODEL : str = "gpt-4o-mini"
    MAX_RETRIES : int = 3
    RAG_DOCUMENT_PATH : str = "data/git_docs.pdf"

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

settings = Settings()