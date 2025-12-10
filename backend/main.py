from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .config.settings import settings
from .api.v1.base_router import api_router
from .database.database import engine, Base
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


limiter = Limiter(key_func=get_remote_address)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    # Create the FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Application startup")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Application shutdown")

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add a global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "An internal server error occurred."},
        )

    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    @app.get("/")
    def read_root():
        return {"message": "Textbook Generation and RAG Chatbot API"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


# Create the application instance
app = create_app()


# If running this file directly, start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )