#!/usr/bin/env python3
"""
Demostración de la estructura de la API sin dependencias externas
Este script muestra como funcionaría el servicio con mocks
"""

import json
from pathlib import Path
from typing import Dict, Any

# Mock de formatos soportados
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

def mock_validate_image_format(image_path: str) -> bool:
    """Mock de validación de formato de imagen"""
    file_extension = Path(image_path).suffix.lower()
    return file_extension in SUPPORTED_IMAGE_FORMATS

def mock_analyze_image_with_gemini(image_path: str, prompt: str) -> Dict[str, Any]:
    """
    Mock del servicio de análisis de Gemini que demuestra la estructura de respuesta
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
    
    # Verificar si el archivo existe
    if not Path(image_path).exists():
        result["error"] = f"El archivo de imagen no se encuentra en la ruta: {image_path}"
        result["error_code"] = "FILE_NOT_FOUND"
        return result
    
    # Validar formato
    if not mock_validate_image_format(image_path):
        result["error"] = f"Formato de imagen no soportado. Formatos válidos: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
        result["error_code"] = "UNSUPPORTED_FORMAT"
        return result
    
    # Simular análisis exitoso
    result["success"] = True
    result["analysis"] = f"""
    Análisis simulado de la imagen '{Path(image_path).name}':
    
    Esta imagen ha sido analizada usando el modelo Gemini AI simulado. 
    Prompt utilizado: "{prompt[:100]}..."
    
    Basándose en el contexto educativo de ESPOL, esta imagen podría relacionarse con:
    
    1. Ingeniería en Computación (FIEC) - Por el análisis de imágenes digitales
    2. Ciencia de Datos e IA (FIEC) - Por el procesamiento inteligente de información
    3. Ingeniería Industrial (FIMCP) - Por la optimización de procesos mediante IA
    
    Recomendación: Los estudiantes interesados en tecnologías de IA y análisis 
    de imágenes encontrarían en la Facultad de Ingeniería Eléctrica y Computación 
    las carreras más alineadas con estas tecnologías emergentes.
    """.strip()
    
    # Agregar metadatos simulados
    try:
        file_stat = Path(image_path).stat()
        result["metadata"].update({
            "file_size": file_stat.st_size,
            "image_size": [800, 600],  # Simulado
            "image_format": "JPEG"     # Simulado
        })
    except:
        pass
    
    return result

def mock_check_gemini_health() -> Dict[str, Any]:
    """Mock del health check del servicio Gemini"""
    import os
    
    health = {
        "service": "gemini",
        "status": "unhealthy",
        "details": {}
    }
    
    # Verificar si hay API key (aunque sea mock)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        health["details"]["error"] = "GEMINI_API_KEY no configurada"
        return health
    
    # Simular servicio saludable
    health["status"] = "healthy"
    health["details"] = {
        "model": "gemini-1.5-flash",
        "supported_formats": list(SUPPORTED_IMAGE_FORMATS),
        "api_key_configured": True
    }
    
    return health

def demo_api_responses():
    """Demuestra las respuestas de la API con diferentes casos"""
    print("🎭 Demostración de Respuestas de la API Gemini")
    print("=" * 50)
    
    # Caso 1: Análisis exitoso
    print("\n📸 Caso 1: Imagen válida encontrada")
    print("-" * 30)
    
    # Crear archivo temporal de imagen para la demo
    test_image = Path("/tmp/test_image.jpg")
    test_image.touch()  # Crear archivo vacío
    
    result1 = mock_analyze_image_with_gemini(
        str(test_image),
        "Analiza esta imagen educativa y recomienda carreras de ESPOL"
    )
    
    print("Respuesta:")
    print(json.dumps(result1, indent=2, ensure_ascii=False))
    
    # Caso 2: Archivo no encontrado
    print("\n🚫 Caso 2: Archivo no encontrado")
    print("-" * 30)
    
    result2 = mock_analyze_image_with_gemini(
        "/ruta/inexistente/imagen.jpg",
        "Describe la imagen"
    )
    
    print("Respuesta:")
    print(json.dumps(result2, indent=2, ensure_ascii=False))
    
    # Caso 3: Formato no soportado
    print("\n📄 Caso 3: Formato no soportado")
    print("-" * 30)
    
    test_pdf = Path("/tmp/document.pdf")
    test_pdf.touch()
    
    result3 = mock_analyze_image_with_gemini(
        str(test_pdf),
        "Analiza este documento"
    )
    
    print("Respuesta:")
    print(json.dumps(result3, indent=2, ensure_ascii=False))
    
    # Health Check
    print("\n🏥 Health Check del Servicio")
    print("-" * 30)
    
    health = mock_check_gemini_health()
    print("Respuesta:")
    print(json.dumps(health, indent=2, ensure_ascii=False))
    
    # Limpiar archivos temporales
    test_image.unlink()
    test_pdf.unlink()

def demo_curl_commands():
    """Muestra ejemplos de comandos curl para probar la API"""
    print("\n🌐 Ejemplos de comandos curl para probar la API")
    print("=" * 50)
    
    examples = [
        {
            "name": "Análisis básico de imagen",
            "command": '''curl -X POST "http://localhost:8000/analyze-image" \\
     -H "accept: application/json" \\
     -H "Content-Type: multipart/form-data" \\
     -F "file=@/ruta/a/imagen.jpg" \\
     -F "prompt=Describe esta imagen educativa"'''
        },
        {
            "name": "Análisis para recomendación de carrera",
            "command": '''curl -X POST "http://localhost:8000/analyze-image" \\
     -H "accept: application/json" \\
     -H "Content-Type: multipart/form-data" \\
     -F "file=@/ruta/a/laboratorio.jpg" \\
     -F "prompt=Analiza este laboratorio y sugiere qué carreras de ESPOL se relacionan mejor"'''
        },
        {
            "name": "Health check general",
            "command": '''curl -X GET "http://localhost:8000/health" \\
     -H "accept: application/json"'''
        },
        {
            "name": "Health check específico de Gemini",
            "command": '''curl -X GET "http://localhost:8000/health/gemini" \\
     -H "accept: application/json"'''
        }
    ]
    
    for example in examples:
        print(f"\n📋 {example['name']}:")
        print(f"```bash\n{example['command']}\n```")

def main():
    """Función principal de demostración"""
    demo_api_responses()
    demo_curl_commands()
    
    print("\n" + "=" * 50)
    print("✨ Funcionalidades implementadas:")
    print("   • Validación de formatos de imagen")
    print("   • Manejo robusto de errores con códigos específicos")  
    print("   • Respuestas estructuradas con metadatos")
    print("   • Health checks para monitoreo")
    print("   • Documentación completa con ejemplos")
    print("   • Logging profesional")
    print("   • Nombres únicos para archivos temporales")
    print("   • Limpieza automática de recursos")

if __name__ == "__main__":
    main()