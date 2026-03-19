import logging

from fastapi import FastAPI
from dotenv import load_dotenv

from app.utils import setup_logging
from app.routes import voice

load_dotenv()


def app_factory() -> FastAPI:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting fastAPI application ...")

    app = FastAPI()
    app.include_router(voice, prefix="/ws")

    return app
