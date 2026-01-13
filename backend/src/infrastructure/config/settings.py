from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Aplicação
    app_name: str = "Finance API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Banco de dados
    database_url: str = "sqlite+aiosqlite:///./finance.db"

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 horas

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]


@lru_cache
def get_settings() -> Settings:
    """Retorna as configurações da aplicação (cached)."""
    return Settings()
