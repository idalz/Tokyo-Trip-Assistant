"""
FastAPI entrypoint for Tokyo Trip Assistant.
Starts FastAPI app and registers routes.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from app.core.config import settings
from app.core.logger import setup_logging
from app.routes.chat import router as chat_router
import logging

# Setup logging and get module-specific logger
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"{settings.APP_NAME} starting up in {settings.environment} mode...")
    yield
    # Shutdown
    logger.info(f"{settings.APP_NAME} shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }

@app.get("/ready")
async def readiness_check():
    # Will check OpenAI, Pinecone, Weather API when implemented
    return {
        "status": "ready",
        "dependencies": {
            "openai": "ok",
            "pinecone": "ok",
            "weather_api": "ok"
        }
    }

@app.get("/")
async def root():
    if settings.environment == "production":
        return {
            "service": settings.APP_NAME,
            "status": "running"
        }

    return {
        "service": settings.APP_NAME,
        "description": settings.DESCRIPTION,
        "version": settings.VERSION,
        "environment": settings.environment,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "readiness": "/ready",
            "documentation": "/docs" if settings.environment != "production" else "disabled"
        }
    }

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
