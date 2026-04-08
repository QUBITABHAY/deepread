# src/deepread/api/__init__.py

from .health import router as health_router
from .query import router as query_router
from .upload import router as upload_router

routers = [
    health_router,
    query_router,
    upload_router,
]
