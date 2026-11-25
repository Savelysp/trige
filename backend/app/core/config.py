from pathlib import Path
from typing import Literal

from pydantic import RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- app ---
    app_name: str = "Trige Support"
    app_env: Literal["dev", "staging", "prod"]
    debug: bool = False
    log_level: str = "INFO"

    # --- secure ---
    secret_key: SecretStr

    # --- infr ---
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: SecretStr
    postgres_db: str
    redis_url: RedisDsn

    # --- HTTP ---
    cors_origins: list[str]


settings = Settings()  # pyright: ignore[reportCallIssue]
