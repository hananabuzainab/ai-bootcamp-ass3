from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.config_parser import settings
from src.logger.logger import logger
from src.core.factories import ModelFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{settings.app_name} - {settings.app_version}")
    logger.info("starting application")

    ModelFactory.get_embeddings()
    ModelFactory.get_llm()

    logger.info("application started successfully")

    yield

    logger.info("application shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="rag for telecoms",
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)