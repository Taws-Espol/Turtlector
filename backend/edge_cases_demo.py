#!/usr/bin/env python3
"""
Test casos límite y demostración de robustez del servicio Gemini
Este archivo demuestra como el servicio maneja diferentes situaciones problemáticas
"""

import json
from pathlib import Path

def demonstrate_edge_cases():
    """Demuestra el manejo de casos límite"""
    
    print("🧪 Casos Límite y Manejo de Errores")
    print("=" * 50)
    
    cases = [
        {
            "name": "Prompt extremadamente largo",
            "description": "Qué pasa con prompts de miles de caracteres",
            "test": "prompt_muy_largo",
            "expected": "El servicio debería manejar prompts largos sin problemas"
        },
        {
            "name": "Prompt vacío",
            "description": "Comportamiento con prompt vacío o solo espacios",
            "test": "prompt_vacio",
            "expected": "Análisis genérico o error controlado"
        },
        {
            "name": "Archivo de imagen corrupto",
            "description": "Archivo que existe pero no es una imagen válida",
            "test": "imagen_corrupta",
            "expected": "Error IMAGE_PROCESSING_ERROR"
        },
        {
            "name": "Imagen extremadamente grande",
            "description": "Imagen que excede límites de memoria/procesamiento",
            "test": "imagen_grande",
            "expected": "Error controlado o procesamiento exitoso"
        },
        {
            "name": "Caracteres especiales en nombres",
            "description": "Archivos con nombres complejos (espacios, acentos, símbolos)",
            "test": "caracteres_especiales",
            "expected": "Procesamiento normal independiente del nombre"
        },
        {
            "name": "Múltiples solicitudes concurrentes",
            "description": "Comportamiento bajo carga",
            "test": "concurrencia",
            "expected": "Manejo apropiado de recursos compartidos"
        },
        {
            "name": "Tiempo de respuesta de Gemini lento",
            "description": "API de Gemini responde muy lentamente",
            "test": "timeout",
            "expected": "Timeout manejado apropiadamente"
        },
        {
            "name": "API Key inválida",
            "description": "Clave de API incorrecta o expirada",
            "test": "api_key_invalida",
            "expected": "Error GEMINI_SERVICE_ERROR con mensaje claro"
        },
        {
            "name": "Cuotas de API excedidas",
            "description": "Límite de solicitudes de Google alcanzado",
            "test": "quota_excedida",
            "expected": "Error específico sobre límites de cuota"
        },
        {
            "name": "Red sin conexión",
            "description": "Sin acceso a internet",
            "test": "sin_conexion",
            "expected": "Error de conectividad claro para el usuario"
        }
    ]
    
    for i, case in enumerate(cases, 1):
        print(f"\n{i}. {case['name']}")
        print(f"   📝 Descripción: {case['description']}")
        print(f"   ✅ Comportamiento esperado: {case['expected']}")

def demonstrate_prompts_for_espol():
    """Demuestra prompts específicos optimizados para ESPOL"""
    
    print("\n🎓 Prompts Optimizados para Carreras ESPOL")
    print("=" * 50)
    
    prompts = {
        "Laboratorio General": """
Analiza esta imagen de laboratorio y determina:

1. ¿Qué tipo de laboratorio es? (química, física, biología, ingeniería, computación)
2. ¿Qué equipos específicos puedes identificar?
3. ¿Qué facultades de ESPOL tienen carreras que utilizarían este tipo de instalación?

Facultades de ESPOL para considerar:
- FIEC: Computación, Telecomunicaciones, Electrónica
- FIMCP: Mecánica, Industrial, Alimentos, Materiales
- FCNM: Química, Matemática, Estadística
- FIMCM: Naval, Oceanografía, Acuicultura
- FCV: Biología, Agrícola
- FICT: Civil, Geología, Minas, Petróleo

Recomienda 2-3 carreras específicas con justificación detallada.
        """,
        
        "Proyecto Estudiantil": """
Observa este proyecto estudiantil y evalúa:

1. ¿Qué disciplinas técnicas están involucradas?
2. ¿Qué nivel de complejidad tiene? (básico, intermedio, avanzado)
3. ¿Qué habilidades técnicas demuestra el estudiante?
4. ¿Qué software o herramientas se utilizaron?

Basándose en tu análisis, sugiere:
- La carrera de ESPOL más apropiada
- Cursos específicos que prepararían para este tipo de proyectos
- Posibles áreas de especialización o tesis

Considera el perfil de egreso de cada carrera de ESPOL.
        """,
        
        "Obra Artística/Diseño": """
Examina esta obra de arte o diseño y analiza:

1. ¿Qué técnicas artísticas o de diseño se utilizaron?
2. ¿Es más orientado a medios digitales o tradicionales?
3. ¿Qué mensaje o concepto comunica?
4. ¿Qué nivel técnico demuestra?

Para las carreras de FADCOM en ESPOL:
- Diseño Gráfico: ¿Se relaciona con identidad visual, publicidad, medios impresos?
- Producción para Medios: ¿Tiene elementos de video, audio, multimedia?
- Diseño de Productos: ¿Muestra innovación en objetos funcionales?

Recomienda la especialización más apropiada con justificación.
        """,
        
        "Entorno Natural/Campo": """
Analiza esta imagen de entorno natural y determina:

1. ¿Qué ecosistema o ambiente se muestra?
2. ¿Qué fenómenos naturales o características geológicas observas?
3. ¿Qué recursos naturales podrían estar presentes?
4. ¿Qué problemas ambientales podrían existir?

Para carreras de ESPOL relacionadas con ambiente:
- Oceanografía (FIMCM): Si involucra ecosistemas marinos
- Acuicultura (FIMCM): Si se relaciona con vida acuática
- Geología (FICT): Si muestra formaciones geológicas
- Minas (FICT): Si hay indicios de recursos minerales
- Biología (FCV): Si destaca biodiversidad
- Ingeniería Agrícola (FCV): Si involucra agricultura sostenible

Sugiere 2-3 carreras con justificación ambiental y técnica.
        """,
        
        "Instalación Industrial": """
Examina esta instalación industrial y analiza:

1. ¿Qué tipo de industria o proceso se muestra?
2. ¿Qué maquinaria o sistemas puedes identificar?
3. ¿Qué procesos de producción o transformación ocurren?
4. ¿Qué consideraciones de seguridad y calidad observas?

Para ingenierías de ESPOL:
- Industrial (FIMCP): Optimización de procesos, gestión de producción
- Mecánica (FIMCP): Sistemas mecánicos, mantenimiento, diseño
- Química (FCNM): Procesos químicos, transformación de materiales  
- Alimentos (FIMCP): Si involucra procesamiento alimentario
- Materiales (FIMCP): Si se enfoca en propiedades de materiales
- Eléctrica (FIEC): Si hay sistemas de control y automatización

Recomienda carreras considerando el tipo de industria específica.
        """
    }
    
    for categoria, prompt in prompts.items():
        print(f"\n📋 {categoria}")
        print("-" * 30)
        print(f"```\n{prompt.strip()}\n```")

def demonstrate_integration_patterns():
    """Demuestra patrones de integración recomendados"""
    
    print("\n🔧 Patrones de Integración Recomendados")
    print("=" * 50)
    
    patterns = [
        {
            "name": "Retry con Backoff Exponencial",
            "description": "Para manejar errores temporales de la API",
            "code": """
import time
import random

async def analyze_with_retry(image_path: str, prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = await analyze_image_with_gemini(image_path, prompt)
            
            if result["success"]:
                return result
                
            # Si el error no es temporal, no reintentar
            if result["error_code"] in ["FILE_NOT_FOUND", "UNSUPPORTED_FORMAT"]:
                return result
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise
                
            # Backoff exponencial con jitter
            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
    
    return {"success": False, "error": "Max retries exceeded"}
            """
        },
        {
            "name": "Validación Previa Completa",
            "description": "Validar todo antes de enviar a Gemini",
            "code": """
def validate_request(file_path: str, prompt: str) -> dict:
    errors = []
    
    # Validar archivo
    if not Path(file_path).exists():
        errors.append("Archivo no encontrado")
    elif not validate_image_format(file_path):
        errors.append("Formato de imagen no soportado")
    elif Path(file_path).stat().st_size > 10_000_000:  # 10MB
        errors.append("Archivo demasiado grande")
    
    # Validar prompt
    if not prompt.strip():
        errors.append("Prompt no puede estar vacío")
    elif len(prompt) > 10000:
        errors.append("Prompt demasiado largo")
    
    return {"valid": len(errors) == 0, "errors": errors}
            """
        },
        {
            "name": "Cache de Resultados",
            "description": "Evitar análisis redundantes",
            "code": """
import hashlib
import json

class GeminiCache:
    def __init__(self):
        self.cache = {}
    
    def get_cache_key(self, image_path: str, prompt: str) -> str:
        # Hash del contenido de la imagen + prompt
        with open(image_path, 'rb') as f:
            image_hash = hashlib.md5(f.read()).hexdigest()
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        return f"{image_hash}_{prompt_hash}"
    
    def get(self, image_path: str, prompt: str):
        key = self.get_cache_key(image_path, prompt)
        return self.cache.get(key)
    
    def set(self, image_path: str, prompt: str, result: dict):
        key = self.get_cache_key(image_path, prompt)
        self.cache[key] = result

# Uso
cache = GeminiCache()

async def analyze_with_cache(image_path: str, prompt: str):
    # Intentar obtener del cache
    cached = cache.get(image_path, prompt)
    if cached:
        return cached
    
    # Si no está en cache, analizar y guardar
    result = await analyze_image_with_gemini(image_path, prompt)
    if result["success"]:
        cache.set(image_path, prompt, result)
    
    return result
            """
        },
        {
            "name": "Monitoreo y Métricas",
            "description": "Tracking de uso y performance",
            "code": """
import time
from collections import defaultdict

class GeminiMetrics:
    def __init__(self):
        self.stats = defaultdict(int)
        self.response_times = []
    
    def record_request(self, success: bool, response_time: float, error_code: str = None):
        self.stats['total_requests'] += 1
        self.stats['successful_requests'] += 1 if success else 0
        self.response_times.append(response_time)
        
        if error_code:
            self.stats[f'error_{error_code}'] += 1
    
    def get_stats(self):
        if not self.response_times:
            return self.stats
            
        return {
            **dict(self.stats),
            'avg_response_time': sum(self.response_times) / len(self.response_times),
            'success_rate': (self.stats['successful_requests'] / self.stats['total_requests']) * 100
        }

# Uso
metrics = GeminiMetrics()

async def analyze_with_metrics(image_path: str, prompt: str):
    start_time = time.time()
    
    try:
        result = await analyze_image_with_gemini(image_path, prompt)
        response_time = time.time() - start_time
        
        metrics.record_request(
            success=result["success"],
            response_time=response_time,
            error_code=result.get("error_code")
        )
        
        return result
        
    except Exception as e:
        response_time = time.time() - start_time
        metrics.record_request(
            success=False,
            response_time=response_time,
            error_code="EXCEPTION"
        )
        raise
            """
        }
    ]
    
    for pattern in patterns:
        print(f"\n🛠️  {pattern['name']}")
        print(f"📝 {pattern['description']}")
        print(f"```python{pattern['code']}\n```")

def main():
    demonstrate_edge_cases()
    demonstrate_prompts_for_espol()
    demonstrate_integration_patterns()
    
    print("\n" + "=" * 50)
    print("📚 Recursos Adicionales:")
    print("   • Documentación completa: backend/docs/gemini_integration_examples.md")
    print("   • Script de pruebas: backend/test_gemini_service.py") 
    print("   • Validación de servicios: backend/validate_gemini_service.py")
    print("   • Health check: GET /health/gemini")
    print("   • API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()