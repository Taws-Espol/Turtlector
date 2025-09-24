import os
import logging
from typing import Dict, Optional, Any
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image

# Configurar logging
logger = logging.getLogger(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración del Modelo Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Formatos de imagen soportados por Gemini
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

# Configuración del modelo (se inicializa bajo demanda)
_model = None

def _get_model():
    """Obtiene el modelo Gemini, inicializándolo si es necesario."""
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró la variable GEMINI_API_KEY. Asegúrate de que está en tu archivo .env")
        
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Modelo Gemini inicializado correctamente")
    
    return _model

def validate_image_format(image_path: str) -> bool:
    """Valida si el formato de imagen es soportado por Gemini."""
    file_extension = Path(image_path).suffix.lower()
    return file_extension in SUPPORTED_IMAGE_FORMATS

def analyze_image_with_gemini(image_path: str, prompt: str) -> Dict[str, Any]:
    """
    Analiza una imagen local utilizando el modelo Gemini y un prompt de texto.

    Args:
        image_path (str): La ruta completa al archivo de la imagen que se va a analizar.
        prompt (str): La instrucción o pregunta que se le hará al modelo sobre la imagen.

    Returns:
        Dict con la respuesta estructurada:
        {
            "success": bool,
            "analysis": str | None,
            "error": str | None,
            "error_code": str | None,
            "metadata": dict
        }
    """
    result = {
        "success": False,
        "analysis": None,
        "error": None,
        "error_code": None,
        "metadata": {
            "image_path": image_path,
            "prompt_length": len(prompt),
            "model": "gemini-1.5-flash"
        }
    }
    
    try:
        # Verificar si el archivo de imagen existe
        image_path_obj = Path(image_path)
        if not image_path_obj.is_file():
            result["error"] = f"El archivo de imagen no se encuentra en la ruta: {image_path}"
            result["error_code"] = "FILE_NOT_FOUND"
            logger.error(f"Archivo no encontrado: {image_path}")
            return result

        # Validar formato de imagen
        if not validate_image_format(image_path):
            result["error"] = f"Formato de imagen no soportado. Formatos válidos: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
            result["error_code"] = "UNSUPPORTED_FORMAT"
            logger.error(f"Formato no soportado: {image_path_obj.suffix}")
            return result

        # Obtener información de la imagen
        try:
            with Image.open(image_path) as img:
                result["metadata"].update({
                    "image_size": img.size,
                    "image_format": img.format,
                    "file_size": image_path_obj.stat().st_size
                })
                
                # Enviar la imagen y el prompt al modelo
                logger.info(f"Analizando imagen '{image_path}' con Gemini")
                model = _get_model()
                response = model.generate_content([prompt, img])
                
                # Verificar que la respuesta tenga contenido
                if not response.text:
                    result["error"] = "Gemini no pudo generar una respuesta para la imagen"
                    result["error_code"] = "EMPTY_RESPONSE"
                    logger.warning("Respuesta vacía de Gemini")
                    return result
                
                result["success"] = True
                result["analysis"] = response.text.strip()
                logger.info("Análisis completado exitosamente")
                
        except Exception as img_error:
            result["error"] = f"Error procesando imagen: {str(img_error)}"
            result["error_code"] = "IMAGE_PROCESSING_ERROR"
            logger.error(f"Error procesando imagen: {img_error}")
            return result

    except Exception as e:
        result["error"] = f"Error interno del servicio Gemini: {str(e)}"
        result["error_code"] = "GEMINI_SERVICE_ERROR"
        logger.error(f"Error del servicio Gemini: {e}")
    
    return result

def check_gemini_health() -> Dict[str, Any]:
    """Verifica el estado del servicio Gemini."""
    health = {
        "service": "gemini",
        "status": "unhealthy",
        "details": {}
    }
    
    try:
        # Verificar API Key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            health["details"]["error"] = "GEMINI_API_KEY no configurada"
            return health
            
        # Intentar inicializar el modelo
        model = _get_model()
        health["status"] = "healthy"
        health["details"] = {
            "model": "gemini-1.5-flash",
            "supported_formats": list(SUPPORTED_IMAGE_FORMATS),
            "api_key_configured": bool(api_key)
        }
        
    except Exception as e:
        health["details"]["error"] = str(e)
        logger.error(f"Health check falló: {e}")
    
    return health