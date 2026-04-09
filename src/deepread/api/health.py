from fastapi import APIRouter
from deepread.core.logger import logger

router = APIRouter()


@router.get("/")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}
