from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from datetime import datetime

from app.config.settings import settings
from app.routers import chat, transcription
from app.models.schemas import (
    HealthResponse,
    ErrorResponse
)

app = FastAPI(
    title=settings.app_name,
    description="API para el proyecto Turtlector que interactúa con IA para orientación vocacional",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

app.include_router(chat.router)
app.include_router(transcription.router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=f"Error {exc.status_code}"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Error interno del servidor",
            detail=str(exc)
        ).dict()
    )

@app.get("/", response_model=HealthResponse)
async def root():
    """
    Endpoint principal de la API.
    """
    return HealthResponse(
        status="running",
        version=settings.app_version
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de verificación de salud de la API.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
