from fastapi import APIRouter
from . import textbook_router, chat_router, index_router, parameter_router


# Create the main API router for version 1
api_router = APIRouter()

# Include all the sub-routers
api_router.include_router(textbook_router.router, prefix="/textbooks", tags=["textbooks"])
api_router.include_router(chat_router.router, prefix="/chat", tags=["chat"])
api_router.include_router(index_router.router, prefix="/index", tags=["index"])
api_router.include_router(parameter_router.router, prefix="/parameters", tags=["parameters"])


# Health check endpoint
@api_router.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy", "version": "1.0.0"}