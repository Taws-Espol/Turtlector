from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from datetime import datetime

from app.config.settings import settings
from app.routers import chat, transcription
from app.services.gemini_service import analyze_image_with_gemini
from app.models.schemas import (
    ImageAnalysisRequest,
    ImageAnalysisResponse,
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
    allow_origins=settings.cors_origins,
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

@app.post("/analyze-image", response_model=ImageAnalysisResponse, tags=["Image Analysis"])
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    prompt: str = "Describe detalladamente lo que ves en esta imagen y cómo se relaciona con las carreras universitarias."
):
    """
    Analiza una imagen usando Gemini AI.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No se proporcionó archivo")

    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)

    temp_file_path = upload_path / file.filename

    try:
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        analysis_result = analyze_image_with_gemini(
            image_path=str(temp_file_path),
            prompt=prompt
        )

        if analysis_result is None:
            raise HTTPException(
                status_code=500,
                detail="El servicio de Gemini no pudo procesar la imagen."
            )

        return ImageAnalysisResponse(
            filename=file.filename,
            analysis=analysis_result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando imagen: {str(e)}")

    finally:
        if temp_file_path.exists():
            os.remove(temp_file_path)

@app.post("/test/analyze-image", response_model=ImageAnalysisResponse, tags=["Tests"])
async def test_analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Endpoint de prueba para análisis de imagen con prompt predefinido.
    """
    test_prompt = """Analiza esta imagen considerando las siguientes carreras de ESPOL:

FADCOM: Diseño Gráfico, Producción para Medios, Diseño de Productos
FCNM: Ingeniería Química, Logística, Estadística, Matemática
FCSH: Administración, Arqueología, Auditoría, Economía, Turismo
FCV: Biología, Ingeniería Agrícola y Biológica, Nutrición
FICT: Ingeniería Civil, Geología, Minas, Petróleo
FIEC: Electricidad, Electrónica, Telecomunicaciones, Computación, Ciencia de Datos
FIMCM: Acuicultura, Ingeniería Naval, Oceanografía
FIMCP: Mecánica, Alimentos, Industrial, Materiales, Mecatrónica

¿Con qué carrera(s) se relaciona mejor esta imagen y por qué?"""

    return await analyze_image_endpoint(file, test_prompt)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )