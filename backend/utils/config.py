from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    GROQ_API_KEY: str
    MODEL_NAME: str = "llama-3.3-70b-versatile" 
    MAX_RETRIES: int = 3
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 2000
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
