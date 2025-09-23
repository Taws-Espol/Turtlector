from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from pathlib import Path
from datetime import datetime

from app.config.settings import settings
from app.routers import chat, transcription
from app.services.gemini_service import analyze_image_with_gemini, check_gemini_health
from app.models.schemas import (
    ImageAnalysisRequest,
    ImageAnalysisResponse,
    ImageAnalysisMetadata,
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

@app.get("/health/gemini", tags=["Health"])
async def gemini_health_check():
    """
    Verifica el estado específico del servicio Gemini AI.
    
    Returns:
        Estado del servicio Gemini con detalles de configuración
    """
    health_result = check_gemini_health()
    
    # Retornar código HTTP apropiado según el estado
    if health_result["status"] == "unhealthy":
        raise HTTPException(
            status_code=503, 
            detail={
                "service": "gemini",
                "status": "unhealthy",
                "error": health_result["details"].get("error", "Unknown error")
            }
        )
    
    return health_result

@app.post("/analyze-image", response_model=ImageAnalysisResponse, tags=["Image Analysis"])
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    prompt: str = "Describe detalladamente lo que ves en esta imagen y cómo se relaciona con las carreras universitarias."
):
    """
    Analiza una imagen usando Gemini AI.
    
    - **file**: Archivo de imagen a analizar (formatos: JPG, JPEG, PNG, GIF, BMP, WEBP)
    - **prompt**: Texto que describe qué análisis realizar sobre la imagen
    
    Returns:
        Respuesta estructurada con el análisis, metadatos y manejo de errores
        
    Example Response:
        ```json
        {
            "success": true,
            "analysis": "Esta imagen muestra un laboratorio de química...",
            "filename": "lab-image.jpg",
            "error": null,
            "error_code": null,
            "metadata": {
                "image_size": [1920, 1080],
                "image_format": "JPEG",
                "file_size": 245760,
                "prompt_length": 95,
                "model": "gemini-1.5-flash"
            }
        }
        ```
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No se proporcionó archivo")

    # Validar formato de archivo
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de archivo no soportado: {file_extension}. Formatos válidos: JPG, JPEG, PNG, GIF, BMP, WEBP"
        )

    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)

    # Generar nombre único para evitar colisiones
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{file.filename}"
    temp_file_path = upload_path / unique_filename

    try:
        # Guardar archivo temporalmente
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analizar imagen con Gemini
        analysis_result = analyze_image_with_gemini(
            image_path=str(temp_file_path),
            prompt=prompt
        )

        # Convertir metadatos del resultado
        metadata = None
        if analysis_result.get("metadata"):
            metadata = ImageAnalysisMetadata(**analysis_result["metadata"])

        # Crear respuesta
        response = ImageAnalysisResponse(
            success=analysis_result["success"],
            analysis=analysis_result["analysis"],
            filename=file.filename,
            error=analysis_result["error"],
            error_code=analysis_result["error_code"],
            metadata=metadata
        )

        # Si no fue exitoso, usar código de error HTTP apropiado
        if not analysis_result["success"]:
            if analysis_result["error_code"] == "FILE_NOT_FOUND":
                raise HTTPException(status_code=404, detail=analysis_result["error"])
            elif analysis_result["error_code"] == "UNSUPPORTED_FORMAT":
                raise HTTPException(status_code=400, detail=analysis_result["error"])
            elif analysis_result["error_code"] in ["EMPTY_RESPONSE", "IMAGE_PROCESSING_ERROR"]:
                raise HTTPException(status_code=422, detail=analysis_result["error"])
            else:
                raise HTTPException(status_code=500, detail=analysis_result["error"])

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno procesando imagen: {str(e)}")

    finally:
        if temp_file_path.exists():
            try:
                os.remove(temp_file_path)
            except OSError:
                pass  # Ignorar errores al eliminar archivo temporal

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