# Servicio TTS (Text-to-Speech)

Este servicio permite convertir texto a voz usando Google Cloud Text-to-Speech API.

## Archivos Principales

- `app/services/tts_service.py` - Clase principal TTSService
- `test_tts_service.py` - Script de prueba y ejemplo de uso

## Configuración

### Variables de Entorno Requeridas

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/archivo-de-credenciales.json"
```

### Dependencias

```bash
pip install google-cloud-texttospeech==2.16.3
```

## Uso Básico

```python
from app.services.tts_service import TTSService

# Crear instancia con voz por defecto
tts = TTSService()

# Convertir texto a audio
audio_file = tts.synthesize_and_save("Tu texto aquí")
```

## Uso Avanzado

```python
# Usar voz específica
tts = TTSService(voice_name="español_españa_femenina")

# Cambiar voz en tiempo real
tts.change_voice("español_estados_unidos_masculina")

# Usar carpeta personalizada
tts = TTSService(output_folder="mi_carpeta_audios")
```

## Voces Disponibles

La clase incluye voces recomendadas en español:

- `español_españa_femenina` - es-ES-Neural2-A
- `español_españa_masculina` - es-ES-Neural2-F
- `español_estados_unidos_femenina` - es-US-Neural2-A
- `español_estados_unidos_masculina` - es-US-Neural2-B (voz por defecto)
- `español_wavenet_femenina` - es-ES-Wavenet-F
- `español_wavenet_masculina` - es-ES-Wavenet-G
- `español_estudio_femenina` - es-ES-Studio-C
- `español_estudio_masculina` - es-ES-Studio-F
- `español_chirp_femenina` - es-ES-Chirp-HD-F
- `español_chirp_masculina` - es-ES-Chirp-HD-D

## Prueba

```bash
python test_tts_service.py
```

## Características

- **Voz por defecto:** es-US-Neural2-B (español masculino Estados Unidos)
- **Formato de audio:** MP3
- **Nomenclatura automática:** respuesta_1.mp3, respuesta_2.mp3, etc.
- **Directorio de salida:** uploads/respuestas/
- **Manejo de errores:** Robusto con mensajes informativos
