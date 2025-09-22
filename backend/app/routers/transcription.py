from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import os
import shutil
import time
from openai import OpenAI
from dotenv import load_dotenv
from app.models.schemas import (
    TranscriptionResponse,
    AudioUploadResponse,
    TranscriptionRequest
)
from app.config.settings import settings
import tempfile
import subprocess

load_dotenv()

router = APIRouter(prefix="/transcription", tags=["Transcription"])

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_audio_duration(file_path: str) -> float:
    """
    Obtiene la duración del archivo de audio usando ffprobe.
    """
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'csv=p=0', file_path
        ], capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 0.0

def validate_audio_file(file: UploadFile) -> bool:
    """
    Valida que el archivo sea un formato de audio soportado.
    """
    allowed_extensions = [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm", ".mp4"]
    file_extension = Path(file.filename).suffix.lower()
    return file_extension in allowed_extensions

@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Sube un archivo de audio al servidor.
    """
    try:
        if not validate_audio_file(file):
            raise HTTPException(
                status_code=400,
                detail="Formato de archivo no soportado. Formatos permitidos: mp3, wav, m4a, ogg, flac, webm, mp4"
            )

        if file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"Archivo demasiado grande. Máximo permitido: {settings.max_file_size / 1024 / 1024:.1f}MB"
            )

        upload_path = Path(settings.upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)

        file_path = upload_path / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        duration = get_audio_duration(str(file_path))

        return AudioUploadResponse(
            filename=file.filename,
            file_size=file.size,
            duration=duration,
            format=Path(file.filename).suffix.lower().replace('.', '')
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo archivo: {str(e)}")

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form(default="es")
):
    """
    Transcribe un archivo de audio usando OpenAI Whisper.
    """
    try:
        if not validate_audio_file(file):
            raise HTTPException(
                status_code=400,
                detail="Formato de archivo no soportado"
            )

        start_time = time.time()

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "rb") as audio_file:
                if language == "auto":
                    transcription = openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json"
                    )
                else:
                    transcription = openai_client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language=language,
                        response_format="verbose_json"
                    )

            processing_time = time.time() - start_time

            if hasattr(transcription, 'text'):
                transcription_text = transcription.text
            else:
                transcription_text = str(transcription)

            return TranscriptionResponse(
                transcription=transcription_text,
                confidence=getattr(transcription, 'confidence', None),
                processing_time=processing_time
            )

        finally:
            os.unlink(temp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en transcripción: {str(e)}")

@router.post("/transcribe-file/{filename}", response_model=TranscriptionResponse)
async def transcribe_uploaded_file(
    filename: str,
    language: str = "es"
):
    """
    Transcribe un archivo de audio previamente subido.
    """
    try:
        file_path = Path(settings.upload_dir) / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        start_time = time.time()

        with open(file_path, "rb") as audio_file:
            if language == "auto":
                transcription = openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
            else:
                transcription = openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json"
                )

        processing_time = time.time() - start_time

        if hasattr(transcription, 'text'):
            transcription_text = transcription.text
        else:
            transcription_text = str(transcription)

        return TranscriptionResponse(
            transcription=transcription_text,
            confidence=getattr(transcription, 'confidence', None),
            processing_time=processing_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en transcripción: {str(e)}")

@router.get("/files")
async def list_audio_files():
    """
    Lista todos los archivos de audio subidos.
    """
    try:
        upload_path = Path(settings.upload_dir)

        if not upload_path.exists():
            return {"files": []}

        audio_files = []
        for file_path in upload_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in settings.allowed_extensions:
                stat_info = file_path.stat()
                audio_files.append({
                    "filename": file_path.name,
                    "size": stat_info.st_size,
                    "created": stat_info.st_ctime,
                    "format": file_path.suffix.lower().replace('.', '')
                })

        return {"files": audio_files}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando archivos: {str(e)}")

@router.delete("/files/{filename}")
async def delete_audio_file(filename: str):
    """
    Elimina un archivo de audio subido.
    """
    try:
        file_path = Path(settings.upload_dir) / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        file_path.unlink()
        return {"message": f"Archivo {filename} eliminado exitosamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando archivo: {str(e)}")

@router.get("/health")
async def transcription_health():
    """
    Verifica el estado del servicio de transcripción.
    """
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return {"status": "unhealthy", "reason": "OpenAI API key not configured"}

        return {
            "status": "healthy",
            "service": "transcription",
            "whisper_model": "whisper-1",
            "supported_formats": settings.allowed_extensions
        }

    except Exception as e:
        return {"status": "unhealthy", "reason": str(e)}