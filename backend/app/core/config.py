from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./airline.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production-use-env-variable"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    PROJECT_NAME: str = "Airline Booking & Operations System"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()

