import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./snake_arena.db"
    )
    
    # JWT settings
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-here-change-in-production"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application settings
    app_name: str = "Snake Arena Online"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


# Global settings instance
settings = Settings()
