#!/usr/bin/env python3
"""
Script de validación para verificar la funcionalidad básica sin API key
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Prueba que todas las importaciones funcionen correctamente"""
    print("🔍 Probando importaciones...")
    
    try:
        from app.services.gemini_service import validate_image_format, check_gemini_health
        print("✅ Importación del servicio Gemini exitosa")
        
        from app.models.schemas import ImageAnalysisResponse, ImageAnalysisMetadata
        print("✅ Importación de esquemas exitosa")
        
        return True
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_validation_functions():
    """Prueba funciones de validación"""
    print("\n🔧 Probando funciones de validación...")
    
    from app.services.gemini_service import validate_image_format
    
    # Prueba formatos válidos
    valid_formats = ['image.jpg', 'photo.jpeg', 'pic.png', 'graphic.gif', 'bitmap.bmp', 'web.webp']
    for filename in valid_formats:
        if validate_image_format(filename):
            print(f"✅ {filename} - formato válido")
        else:
            print(f"❌ {filename} - debería ser válido")
            return False
    
    # Prueba formatos inválidos
    invalid_formats = ['doc.pdf', 'video.mp4', 'audio.mp3', 'text.txt']
    for filename in invalid_formats:
        if not validate_image_format(filename):
            print(f"✅ {filename} - formato inválido (correcto)")
        else:
            print(f"❌ {filename} - debería ser inválido")
            return False
    
    return True

def test_health_check():
    """Prueba el health check sin API key"""
    print("\n🏥 Probando health check...")
    
    # Temporalmente remover la API key para probar el manejo de errores
    original_key = os.environ.pop('GEMINI_API_KEY', None)
    
    try:
        from app.services.gemini_service import check_gemini_health
        health = check_gemini_health()
        
        print(f"Estado: {health['status']}")
        if health['status'] == 'unhealthy':
            print("✅ Health check maneja correctamente la ausencia de API key")
            print(f"   Error reportado: {health['details'].get('error', 'N/A')}")
            return True
        else:
            print("❌ Health check debería reportar estado unhealthy sin API key")
            return False
            
    finally:
        # Restaurar API key si existía
        if original_key:
            os.environ['GEMINI_API_KEY'] = original_key

def test_schemas():
    """Prueba la creación de esquemas de respuesta"""
    print("\n📋 Probando esquemas de datos...")
    
    try:
        from app.models.schemas import ImageAnalysisResponse, ImageAnalysisMetadata
        
        # Crear metadatos de ejemplo
        metadata = ImageAnalysisMetadata(
            image_path="/test/image.jpg",
            image_size=(800, 600),
            image_format="JPEG",
            file_size=102400,
            prompt_length=50,
            model="gemini-1.5-flash"
        )
        
        # Crear respuesta exitosa
        response_success = ImageAnalysisResponse(
            success=True,
            analysis="Esta es una imagen de prueba",
            filename="test.jpg",
            error=None,
            error_code=None,
            metadata=metadata
        )
        
        # Crear respuesta de error
        response_error = ImageAnalysisResponse(
            success=False,
            analysis=None,
            filename="error.pdf",
            error="Formato no soportado",
            error_code="UNSUPPORTED_FORMAT",
            metadata=None
        )
        
        print("✅ Esquemas de respuesta creados correctamente")
        print(f"   Respuesta exitosa: success={response_success.success}")
        print(f"   Respuesta de error: error_code={response_error.error_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando esquemas: {e}")
        return False

def main():
    """Función principal de validación"""
    print("🐢 Turtlector - Validación de Servicios Gemini AI")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Funciones de validación", test_validation_functions), 
        ("Health check", test_health_check),
        ("Esquemas de datos", test_schemas),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VALIDACIONES:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 Todas las validaciones pasaron exitosamente!")
        print("   El servicio Gemini está listo para uso con API key válida.")
    else:
        print("\n⚠️  Algunas validaciones fallaron. Revisa los errores arriba.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)