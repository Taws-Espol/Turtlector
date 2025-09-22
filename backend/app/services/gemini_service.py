import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# --- Configuración del Modelo Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validar que la API Key esté configurada
if not GEMINI_API_KEY:
    raise ValueError("No se encontró la variable  GEMINI_API_KEY. Asegúrate de que está en tu archivo .env")

genai.configure(api_key=GEMINI_API_KEY)

# Usamos un modelo optimizado para visión y texto

model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_image_with_gemini(image_path: str, prompt: str) -> str | None:
    """
    Analiza una imagen local utilizando el modelo Gemini y un prompt de texto.

    Args:
        image_path (str): La ruta completa al archivo de la imagen que se va a analizar.
        prompt (str): La instrucción o pregunta que se le hará al modelo sobre la imagen.

    Returns:
        El texto generado por el modelo como respuesta, o None si ocurre un error.
    """
    try:
        # Verificar si el archivo de imagen existe
        if not Path(image_path).is_file():
            print(f"Error: El archivo de imagen no se encuentra en la ruta: {image_path}")
            return None

        # Abrir la imagen con Pillow 
        img = Image.open(image_path)

        # Enviar la imagen y el prompt al modelo
        print(f"Enviando imagen '{image_path}' a Gemini con el prompt: '{prompt}'")
        response = model.generate_content([prompt, img])
        
        # Devolver el texto de la respuesta
        return response.text

    except Exception as e:
        # Capturar cualquier otro error durante el proceso (ej. error de API, imagen corrupta)
        print(f" Ocurrió un error al procesar con Gemini: {e}")
        return None