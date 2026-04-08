from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()

    # Send to ingestion

    return {"filename": file.filename, "content": content}
