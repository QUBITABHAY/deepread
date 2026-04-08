import uvicorn
from fastapi import FastAPI

from deepread.api import health, query, upload

app = FastAPI(title="DeepRead API")

app.include_router(health.router)
app.include_router(query.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("deepread.main:app", host="0.0.0.0", port=8080, reload=True)