from contextlib import asynccontextmanager

from fastapi import FastAPI
from structlog import get_logger

from app.core.config import settings
from app.core.logging import configure_logging

configure_logging(settings.log_level, json_logs=not settings.debug)
log = get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    log.info("app_started", env=settings.app_env)
    yield
    log.info("app_stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/healthz", tags=["ops"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
