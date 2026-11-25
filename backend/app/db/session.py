from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


def build_dsn(*, database: str | None = None) -> URL:
    return URL.create(
        "postgresql+asyncpg",
        username=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=database or settings.postgres_db,
    )


def create_db_engine(*, database: str | None = None) -> AsyncEngine:
    return create_async_engine(
        build_dsn(database=database),
        pool_pre_ping=True,
    )
