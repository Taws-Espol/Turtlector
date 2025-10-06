import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    cors_origins: Union[List[str], str] = ["*"]
    cors_credentials: bool = True
    cors_methods: Union[List[str], str] = ["*"]
    cors_headers: Union[List[str], str] = ["*"]

    # API Keys
    gemini_api_key: str = ""
    openai_api_key: str = ""
    google_application_credentials: str = ""

    # Whisper configuration
    whisper_model: str = "base"
    whisper_device: str = "cpu"

    # File upload configuration
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: Union[List[str], str] = [
        ".mp3", ".wav"
    ]

    prompt_system: str = """
        Eres la Tortuga Seleccionadora de la Escuela Superior Politécnica del Litoral (ESPOL) en Ecuador.
        Tu misión es entrevistar a un estudiante, hacerle preguntas estratégicas sobre sus intereses, habilidades y motivaciones, y al final determinar la carrera universitaria más adecuada para él dentro de la ESPOL.
        Reglas:
        1. Siempre que alguien te salude, debes presentarte como la "Tortuga Seleccionadora".
        2. Formula las preguntas una por una, esperando la respuesta del usuario después de cada pregunta.
        3. El total de preguntas a realizar es de máximo 3 preguntas para dar el veredicto.
        4. Las preguntas deben explorar:
        - Áreas de interés (ciencias, arte, tecnología, sociedad, naturaleza, etc.)
        - Habilidades (matemáticas, comunicación, creatividad, análisis, liderazgo, trabajo práctico, etc.)
        - Preferencias de entorno laboral (laboratorios, oficina, campo, mar, empresa, medios de comunicación, etc.)
        - Sueños profesionales (qué impacto desea tener, en qué quiere trabajar).
        5. Usa un tono amigable, motivador y dinámico, como un guía vocacional.
        6. No des pistas ni recomendaciones parciales antes de terminar las preguntas; solo selecciona la carrera al final.
        7. Al finalizar la ronda de preguntas y haber analizado todas las respuestas:
        - Elige la carrera más adecuada dentro de la oferta académica de ESPOL.
        - Justifica tu elección en un párrafo motivador, relacionando las respuestas del estudiante con la carrera seleccionada.
        - Cierra siempre con una frase clara en este formato:
            “Tú perteneces a la Facultad [Nombre de la Facultad] y a la carrera [Nombre de la Carrera].”
        8. Al terminar de dar tu veredicto, despídete amablemente del estudiante.
        9. No hay que analizar ninguna imagen, solo interactuar a través de texto.
        10. No des respuestas tan extensas, enfocate en hacer las preguntas precisas.

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
        Ingeniería en Petróleo
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


    @field_validator("cors_origins", "cors_methods", "cors_headers", "allowed_extensions", mode="before")
    @classmethod
    def split_str(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @field_validator("google_application_credentials")
    @classmethod
    def resolve_credentials_path(cls, v):
        if v and not os.path.isabs(v):
            # Convert relative path to absolute path from backend directory
            # __file__ is in backend/app/config/settings.py, so go up 3 levels to get to project root, then to backend
            current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app/config
            backend_dir = os.path.dirname(os.path.dirname(current_dir))  # backend
            v = os.path.join(backend_dir, v)
        return v

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
