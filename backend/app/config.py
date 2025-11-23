import os
import sys
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


def _get_default_database_url() -> str:
    """Get default database URL based on environment"""
    # Use file-based SQLite for tests to ensure tables persist across connections
    if "pytest" in sys.modules or os.getenv("TESTING") == "true":
        return "sqlite:///./test.db"
    
    # Use PostgreSQL for production/Docker
    return "postgresql://snakearena:snakearena@postgres:5432/snakearena"


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # Database settings
    database_url: str = os.getenv(
        "DATABASE_URL", 
        _get_default_database_url()
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
