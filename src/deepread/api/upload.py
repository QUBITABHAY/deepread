from fastapi import APIRouter, File, UploadFile
from deepread.core.logger import logger
from deepread.services.ingestion import ingest_file

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    logger.info(f"Received file upload endpoint hit: {file.filename}")
    
    # Send to ingestion service layer
    result = await ingest_file(file)

    logger.info(f"Ingestion finished for {file.filename}")
    return result
