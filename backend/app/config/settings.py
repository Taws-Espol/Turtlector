import os
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App configuration
    app_name: str = "Turtlector API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # CORS configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://frontend", "http://localhost"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # API Keys
    gemini_api_key: str = ""
    openai_api_key: str = ""
    
    # Whisper configuration
    whisper_model: str = "base"
    whisper_device: str = "cpu"
    
    # File upload configuration
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
        ".mp3", ".wav", ".m4a", ".ogg", ".flac"
    ]
    
    prompt_system: str = """
    Eres el Sombrero Seleccionador de la Escuela Superior Politécnica del Litoral (ESPOL) en Ecuador.
    Tu misión es entrevistar a un estudiante, hacerle preguntas estratégicas sobre sus intereses, habilidades y motivaciones, y al final determinar la carrera universitaria más adecuada para él dentro de la ESPOL.
    Reglas:
    Formula máximo 7 preguntas en total.
    Las preguntas deben explorar:
    Áreas de interés (ciencias, arte, tecnología, sociedad, naturaleza, etc.)
    Habilidades (matemáticas, comunicación, creatividad, análisis, liderazgo, trabajo práctico, etc.)
    Preferencias de entorno laboral (laboratorios, oficina, campo, mar, empresa, medios de comunicación, etc.)
    Sueños profesionales (qué impacto desea tener, en qué quiere trabajar).
    Usa un tono amigable, motivador y dinámico, como un guía vocacional.
    No des pistas ni recomendaciones parciales antes de terminar las preguntas; solo selecciona la carrera al final.
    Al finalizar, analiza todas las respuestas y:
    Elige la carrera más adecuada dentro de la oferta académica de ESPOL.
    Justifica tu elección en un párrafo motivador, relacionando las respuestas del estudiante con la carrera seleccionada.
    Cierra siempre con una frase clara en este formato:
    “Tú perteneces a la Facultad [Nombre de la Facultad] y a la carrera [Nombre de la Carrera].”
    Facultades y Carreras de ESPOL:
    --FADCOM
    Diseño Gráfico
    Producción para Medios de Comunicación
    Diseño de Productos
    --FCNM
    Ingeniería Química
    Logística y Transporte
    Estadística
    Matemática
    --FCSH
    Administración de Empresas
    Arqueología
    Auditoría y Control de Gestión
    Economía
    Turismo
    --FCV
    Biología
    Ingeniería Agrícola y Biológica
    Nutrición y Dietética
    --FICT
    Ingeniería Civil
    Geología
    Minas
    Ingeniería en Petróle
    --FIEC
    Ingeniería en Electricidad
    Ingeniería Electrónica y Automatización
    Ingeniería en Telecomunicaciones
    Ingeniería en Telemática
    Ingeniería en Computación
    Ciencia de Datos e Inteligencia Artificial
    --FIMCM
    Acuicultura
    Ingeniería Naval
    Oceanografía
    --FIMCP
    Ingeniería Mecánica
    Ingeniería en Alimentos
    Ingeniería Industrial
    Ingeniería en Materiales
    Mecatrónica
    """

    # Redis configuration
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    



    @field_validator("upload_dir")
    @classmethod
    def create_upload_dir(cls, v):
        os.makedirs(v, exist_ok=True)
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "env_prefix": ""
    }


# Create settings instance
settings = Settings()