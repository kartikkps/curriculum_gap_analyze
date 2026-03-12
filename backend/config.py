from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./curriculum.db"
    LLM_API_KEY: str = "dummy_key"
    class Config:
        env_file = ".env"

settings = Settings()
