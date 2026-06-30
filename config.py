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

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

settings = Settings()