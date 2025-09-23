#!/usr/bin/env python3
"""
Script de ejemplo para probar el servicio Gemini AI
Este script demuestra cómo usar el servicio desde código Python
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.gemini_service import analyze_image_with_gemini, check_gemini_health

def test_gemini_health():
    """Prueba el health check del servicio Gemini"""
    print("🔍 Verificando estado del servicio Gemini...")
    
    health = check_gemini_health()
    print(f"Estado: {health['status']}")
    
    if health['status'] == 'healthy':
        print("✅ Servicio Gemini funcionando correctamente")
        print(f"   - Modelo: {health['details']['model']}")
        print(f"   - Formatos soportados: {', '.join(health['details']['supported_formats'])}")
        print(f"   - API Key configurada: {health['details']['api_key_configured']}")
        return True
    else:
        print(f"❌ Servicio Gemini no disponible: {health['details'].get('error', 'Error desconocido')}")
        return False

def create_sample_image():
    """Crea una imagen de ejemplo simple para pruebas"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import tempfile
        
        # Crear una imagen simple con texto
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Agregar texto
        text = "LABORATORIO DE QUÍMICA\nESPOL\n\nEquipos:\n• Microscopio\n• Balanza\n• Reactivos"
        draw.text((20, 20), text, fill='black')
        
        # Guardar en archivo temporal
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(temp_file.name)
        return temp_file.name
        
    except ImportError:
        print("⚠️  PIL no disponible. No se puede crear imagen de ejemplo.")
        return None
    except Exception as e:
        print(f"⚠️  Error creando imagen de ejemplo: {e}")
        return None

def test_image_analysis(image_path=None):
    """Prueba el análisis de imagen"""
    print("\n🖼️  Probando análisis de imagen...")
    
    # Si no se proporciona imagen, crear una de ejemplo
    if not image_path:
        print("No se proporcionó imagen. Creando imagen de ejemplo...")
        image_path = create_sample_image()
        
    if not image_path or not os.path.exists(image_path):
        print("❌ No se puede proceder sin una imagen válida")
        return False
        
    # Prompt de ejemplo para análisis educativo
    prompt = """
    Analiza esta imagen y determina:
    1. ¿Qué tipo de entorno o equipamiento se muestra?
    2. ¿Qué carreras universitarias de ESPOL se relacionan mejor con esto?
    3. ¿Qué habilidades específicas se desarrollarían en este contexto?
    
    Proporciona recomendaciones concretas de 2-3 carreras de ESPOL.
    """
    
    print(f"📁 Analizando archivo: {Path(image_path).name}")
    print(f"📝 Prompt: {prompt.strip()[:100]}...")
    
    # Ejecutar análisis
    result = analyze_image_with_gemini(image_path, prompt)
    
    # Mostrar resultados
    if result["success"]:
        print("✅ Análisis completado exitosamente")
        print("\n📊 Resultado del análisis:")
        print("-" * 50)
        print(result["analysis"])
        print("-" * 50)
        
        # Mostrar metadatos
        if result["metadata"]:
            print("\n📋 Metadatos:")
            metadata = result["metadata"]
            for key, value in metadata.items():
                if key == "image_size" and value:
                    print(f"   • Tamaño de imagen: {value[0]} x {value[1]} píxeles")
                elif key == "file_size" and value:
                    print(f"   • Tamaño de archivo: {value:,} bytes")
                elif key == "image_format" and value:
                    print(f"   • Formato: {value}")
                elif key == "model":
                    print(f"   • Modelo: {value}")
                elif key == "prompt_length":
                    print(f"   • Longitud del prompt: {value} caracteres")
        
        return True
    else:
        print(f"❌ Error en el análisis: {result['error']}")
        print(f"   Código de error: {result['error_code']}")
        return False

def main():
    """Función principal que ejecuta las pruebas"""
    print("🐢 Turtlector - Prueba del Servicio Gemini AI")
    print("=" * 50)
    
    # Verificar health check
    if not test_gemini_health():
        print("\n⚠️  Servicio no disponible. Verifica:")
        print("   1. Variable GEMINI_API_KEY en .env")
        print("   2. Conexión a internet")
        print("   3. Validez de la API key")
        return False
    
    # Obtener imagen de los argumentos o usar imagen de ejemplo
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            print(f"⚠️  Archivo no encontrado: {image_path}")
            image_path = None
    
    # Ejecutar análisis de imagen
    success = test_image_analysis(image_path)
    
    # Limpiar archivo temporal si se creó
    if image_path and "tmp" in image_path:
        try:
            os.unlink(image_path)
        except:
            pass
    
    if success:
        print("\n🎉 Todas las pruebas completadas exitosamente!")
        return True
    else:
        print("\n❌ Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    print("Uso:")
    print("  python test_gemini_service.py")
    print("  python test_gemini_service.py /ruta/a/imagen.jpg")
    print()
    
    success = main()
    sys.exit(0 if success else 1)