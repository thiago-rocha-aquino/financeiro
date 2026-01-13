from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config import get_settings
from src.infrastructure.database.database import get_database
from src.presentation.api import (
    auth_router,
    budgets_router,
    categories_router,
    transactions_router,
    users_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Gerencia o ciclo de vida da aplicação."""
    database = get_database()
    await database.create_tables()
    yield


def create_app() -> FastAPI:
    """Factory para criar a aplicação FastAPI."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API de Controle Financeiro Pessoal",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(users_router, prefix=api_prefix)
    app.include_router(categories_router, prefix=api_prefix)
    app.include_router(transactions_router, prefix=api_prefix)
    app.include_router(budgets_router, prefix=api_prefix)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "healthy"}

    return app


app = create_app()
