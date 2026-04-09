from fastapi import APIRouter, File, UploadFile
from deepread.core.logger import logger

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    logger.info(f"Received file upload: {file.filename}")
    content = await file.read()

    # Send to ingestion
    logger.info(f"File {file.filename} read into memory, size: {len(content)} bytes")

    return {"filename": file.filename, "content": content}
