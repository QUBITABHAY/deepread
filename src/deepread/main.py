import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from deepread.api import health, query, upload
from deepread.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Allow the browser to call the API from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(upload.router, prefix="/api")

# Serve the custom HTML UI at http://localhost:8080/
_INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")

@app.get("/", include_in_schema=False)
async def serve_ui():
    """Serves the DeepRead single-page UI."""
    with open(_INDEX, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run("deepread.main:app", host=settings.HOST, port=settings.PORT, reload=True)