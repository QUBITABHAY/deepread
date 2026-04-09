import uvicorn
from fastapi import FastAPI

from deepread.api import health, query, upload
from deepread.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(health.router)
app.include_router(query.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("deepread.main:app", host=settings.HOST, port=settings.PORT, reload=True)