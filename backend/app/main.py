
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
from pathlib import Path
from services.whisper_service import grabar_y_transcribir_audio
# --- Importar Gemini ---
from app.services.gemini_service import analyze_image_with_gemini

# --- Suponiendo que tienes la configuraci�n del directorio de subidas ---
# la variable UPLOAD_DIR debe estar configurada
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


app = FastAPI(
    title="Turtlector API",
    description="API para el proyecto Turtlector que interact�a con IA.",
    version="1.0.0"
)

# --- Endpoint de prueba para el servicio de Gemini ---

@app.post("/test/analyze-image", tags=["Tests"])
async def test_analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Endpoint de prueba para subir una imagen y obtener su an�lisis con Gemini.
    """
    # Crear el directorio de subidas si no existe
    upload_path = Path(UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Ruta temporal para guardar el archivo
    temp_file_path = upload_path / file.filename
    
    try:
        # Guardar el archivo subido en el servidor
        with temp_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -------------------------------------------------------------------
        # DEFINIR EL PROMPT QUE QUIERES USAR PARA LA PRUEBA
        # TODO: Reemplaza este prompt con la pregunta espec�fica
        # Por ejemplo: "�Qu� carrera universitaria se relaciona con esta imagen?"
        # o "Describe la personalidad de alguien que dibujar�a esto."
        test_prompt = "Describe detalladamente lo que ves en esta imagen."
        # -------------------------------------------------------------------

        # Llamar al servicio con la ruta del archivo y el prompt de prueba
        analysis_result = analyze_image_with_gemini(
            image_path=str(temp_file_path),
            prompt=test_prompt
        )

        # Si el servicio falla, devuelve un error "500"
        if analysis_result is None:
            raise HTTPException(
                status_code=500, 
                detail="El servicio de Gemini no pudo procesar la imagen."
            )
        
        # Resultado esperado
        return {"filename": file.filename, "analysis": analysis_result}

    finally:
        # Eliminar archivo despues de eliminar
        if temp_file_path.exists():
            os.remove(temp_file_path)

