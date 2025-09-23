# Integración con Gemini AI - Ejemplos y Documentación

## Descripción General

El servicio Gemini AI en Turtlector permite analizar imágenes para proporcionar análisis educativo y recomendaciones de carreras. Esta documentación presenta ejemplos de integración desde diferentes perspectivas.

## Configuración Requerida

### Variables de Entorno

Asegúrate de configurar la siguiente variable en tu archivo `.env`:

```env
GEMINI_API_KEY=tu_clave_de_gemini_aqui
```

### Formatos de Imagen Soportados

- JPG/JPEG
- PNG
- GIF
- BMP
- WEBP

## Ejemplos de Integración

### 1. Uso desde Python (Backend)

```python
from app.services.gemini_service import analyze_image_with_gemini

# Análisis básico de imagen
result = analyze_image_with_gemini(
    image_path='uploads/lab_image.jpg', 
    prompt='Describe detalladamente lo que ves en esta imagen y cómo se relaciona con las carreras universitarias.'
)

if result["success"]:
    print(f"Análisis: {result['analysis']}")
    print(f"Metadatos: {result['metadata']}")
else:
    print(f"Error: {result['error']} (Código: {result['error_code']})")
```

### 2. Solicitudes HTTP con curl

#### Análisis de Imagen

```bash
# Ejemplo básico
curl -X POST "http://localhost:8000/analyze-image" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/image.jpg" \
     -F "prompt=Describe esta imagen educativa"

# Ejemplo con prompt personalizado para carreras ESPOL
curl -X POST "http://localhost:8000/analyze-image" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/lab_equipment.jpg" \
     -F "prompt=Analiza este laboratorio y determina qué carreras de ESPOL se relacionan mejor con el equipo y actividades mostradas"
```

#### Health Check del Servicio Gemini

```bash
curl -X GET "http://localhost:8000/health/gemini" \
     -H "accept: application/json"
```

### 3. Integración desde Frontend (JavaScript)

```javascript
// Función para analizar imagen
async function analyzeImage(imageFile, customPrompt = null) {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    if (customPrompt) {
        formData.append('prompt', customPrompt);
    }

    try {
        const response = await fetch('/analyze-image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.success) {
            console.log('Análisis:', result.analysis);
            console.log('Metadatos:', result.metadata);
            return result;
        } else {
            console.error('Error en análisis:', result.error);
            throw new Error(result.error);
        }
    } catch (error) {
        console.error('Error de red:', error);
        throw error;
    }
}

// Uso del frontend
const fileInput = document.getElementById('imageInput');
const file = fileInput.files[0];

analyzeImage(file, "¿Qué carrera de ESPOL recomendarías para alguien interesado en esto?")
    .then(result => {
        document.getElementById('analysis-result').textContent = result.analysis;
    })
    .catch(error => {
        document.getElementById('error-message').textContent = error.message;
    });
```

## Ejemplos de Respuesta

### Respuesta Exitosa

```json
{
    "success": true,
    "analysis": "Esta imagen muestra un laboratorio de química con equipos modernos incluyendo balanzas analíticas, campanas extractoras y reactivos organizados. Este entorno se relaciona directamente con las carreras de Ingeniería Química y Ingeniería en Alimentos de la FCNM de ESPOL. Los estudiantes de estas carreras trabajarían regularmente con este tipo de equipamiento para análisis cuantitativos, síntesis de compuestos y desarrollo de productos alimentarios.",
    "filename": "lab_quimico.jpg",
    "error": null,
    "error_code": null,
    "metadata": {
        "image_path": "/uploads/20241201_143022_lab_quimico.jpg",
        "image_size": [1920, 1080],
        "image_format": "JPEG",
        "file_size": 245760,
        "prompt_length": 95,
        "model": "gemini-1.5-flash"
    }
}
```

### Respuesta con Error

```json
{
    "success": false,
    "analysis": null,
    "filename": "documento.pdf",
    "error": "Formato de imagen no soportado. Formatos válidos: .jpg, .jpeg, .png, .gif, .bmp, .webp",
    "error_code": "UNSUPPORTED_FORMAT",
    "metadata": null
}
```

## Casos de Uso Específicos para ESPOL

### 1. Análisis de Laboratorios
```python
prompt_laboratorio = """
Analiza este laboratorio y determina:
1. Qué tipo de laboratorio es (química, física, biología, ingeniería)
2. Qué carreras de ESPOL se beneficiarían más de este equipo
3. Qué habilidades específicas se desarrollarían aquí
4. Recomienda 2-3 carreras específicas con justificación
"""
```

### 2. Análisis de Proyectos Estudiantiles
```python
prompt_proyecto = """
Observa este proyecto estudiantil y analiza:
1. Qué disciplinas técnicas están involucradas
2. Qué facultades de ESPOL tienen carreras relacionadas
3. Qué competencias se demuestran
4. Sugiere el perfil de carrera más adecuado
"""
```

## Manejo de Errores

### Códigos de Error Comunes

- `FILE_NOT_FOUND`: El archivo de imagen no existe
- `UNSUPPORTED_FORMAT`: Formato de imagen no compatible
- `IMAGE_PROCESSING_ERROR`: Error al procesar la imagen
- `EMPTY_RESPONSE`: Gemini no generó respuesta
- `GEMINI_SERVICE_ERROR`: Error interno del servicio

## Health Checks

### Verificación del Servicio

```bash
# Verificar estado del servicio Gemini
curl -X GET "http://localhost:8000/health/gemini"

# Respuesta esperada (servicio saludable)
{
    "service": "gemini",
    "status": "healthy",
    "details": {
        "model": "gemini-1.5-flash",
        "supported_formats": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "api_key_configured": true
    }
}
```

## Mejores Prácticas

### 1. Optimización de Prompts
- Sé específico sobre qué análisis necesitas
- Menciona el contexto educativo de ESPOL
- Solicita recomendaciones concretas de carreras

### 2. Manejo de Archivos
- Valida el formato antes de enviar
- Implementa límites de tamaño de archivo
- Limpia archivos temporales

### 3. Error Handling
- Implementa reintentos para errores temporales
- Proporciona mensajes de error útiles al usuario
- Registra errores para debugging

## Límites y Consideraciones

- **Tamaño máximo**: 10MB por imagen
- **Rate limiting**: Respeta los límites de la API de Gemini
- **Costo**: Monitorea el uso de tokens de la API
- **Calidad**: Imágenes de mayor resolución generan mejores análisis