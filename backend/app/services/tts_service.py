import os
from google.cloud import texttospeech
from pathlib import Path
from app.config.settings import settings

class TTSService:
    """
    Un servicio para convertir texto a voz y guardarlo localmente.
    Utiliza Google Cloud Text-to-Speech API para generar audio en español.
    """

    # Voces recomendadas en español
    RECOMMENDED_VOICES = {
        "español_españa_femenina": "es-ES-Neural2-A",
        "español_españa_masculina": "es-ES-Neural2-F",
        "español_estados_unidos_femenina": "es-US-Neural2-A",
        "español_estados_unidos_masculina": "es-US-Neural2-B",
        "español_wavenet_femenina": "es-ES-Wavenet-F",
        "español_wavenet_masculina": "es-ES-Wavenet-G",
        "español_estudio_femenina": "es-ES-Studio-C",
        "español_estudio_masculina": "es-ES-Studio-F",
        "español_chirp_femenina": "es-ES-Chirp-HD-F",
        "español_chirp_masculina": "es-ES-Chirp-HD-D"
    }

    def __init__(self, output_folder="uploads/respuestas", voice_name=None):
        """
        Inicializa el servicio y se asegura de que la carpeta de salida exista.

        Args:
            output_folder (str): Carpeta donde se guardarán los archivos de audio
            voice_name (str): Nombre de la voz a usar. Si es None, usa voz por defecto.
                             Puede ser un nombre completo (ej: "es-ES-Neural2-A") o
                             un alias de las voces recomendadas.
        """
        # Configurar la variable de entorno si está definida en settings
        if settings.google_application_credentials:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

        self.client = texttospeech.TextToSpeechClient()
        self.output_folder = output_folder
        self.voice_name = voice_name or "es-US-Neural2-B"  # Voz por defecto: español masculino Estados Unidos

        # Si es un alias de voz recomendada, convertir al nombre real
        if self.voice_name in self.RECOMMENDED_VOICES:
            self.voice_name = self.RECOMMENDED_VOICES[self.voice_name]

        # Crea el directorio de salida si no existe
        os.makedirs(self.output_folder, exist_ok=True)
        print(f"Carpeta de salida: '{self.output_folder}' está lista.")
        print(f"Voz seleccionada: {self.voice_name}")

    def _get_next_filename(self) -> str:
        """
        Calcula el siguiente nombre de archivo secuencial (respuesta_1.mp3, respuesta_2.mp3, etc.).

        Returns:
            str: Ruta completa del siguiente archivo a crear
        """
        if not os.path.exists(self.output_folder):
            return os.path.join(self.output_folder, "respuesta_1.mp3")

        files = [f for f in os.listdir(self.output_folder) if f.startswith("respuesta_") and f.endswith(".mp3")]
        if not files:
            return os.path.join(self.output_folder, "respuesta_1.mp3")

        # Extrae los números de los nombres de archivo y encuentra el máximo
        max_num = 0
        for f in files:
            try:
                num_str = f.replace("respuesta_", "").replace(".mp3", "")
                num = int(num_str)
                if num > max_num:
                    max_num = num
            except ValueError:
                continue # Ignora archivos que no sigan el patrón numérico

        next_num = max_num + 1
        return os.path.join(self.output_folder, f"respuesta_{next_num}.mp3")

    def synthesize_and_save(self, text: str) -> str | None:
        """
        Recibe un texto, genera el audio MP3 y lo guarda en un archivo.

        Args:
            text (str): El texto a convertir a voz

        Returns:
            str: La ruta completa del archivo guardado, o None si hay error
        """
        if not text or not text.strip():
            print("Error: El texto no puede estar vacío.")
            return None

        try:
            # Configuración de entrada
            synthesis_input = texttospeech.SynthesisInput(text=text.strip())

            # Configuración de voz
            # Extraer el código de idioma del nombre de la voz
            language_code = self.voice_name.split('-')[0] + '-' + self.voice_name.split('-')[1]

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=self.voice_name
            )

            # Configuración de audio
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            print("Generando audio... (esto puede tardar unos segundos)")
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Obtiene el nombre del archivo y lo guarda
            output_path = self._get_next_filename()
            with open(output_path, "wb") as out:
                out.write(response.audio_content)

            print(f"¡Éxito! Audio guardado en: {output_path}")
            return output_path

        except Exception as e:
            print(f"Error al generar audio: {str(e)}")
            return None

    def list_generated_files(self) -> list:
        """
        Lista todos los archivos de audio generados.

        Returns:
            list: Lista de archivos MP3 en la carpeta de respuestas
        """
        if not os.path.exists(self.output_folder):
            return []

        files = [f for f in os.listdir(self.output_folder) if f.endswith(".mp3")]
        return sorted(files)

    def clear_responses(self) -> bool:
        """
        Elimina todos los archivos de audio generados.

        Returns:
            bool: True si se eliminaron archivos, False si no había archivos
        """
        if not os.path.exists(self.output_folder):
            return False

        files = [f for f in os.listdir(self.output_folder) if f.endswith(".mp3")]
        if not files:
            print("No hay archivos de audio para eliminar.")
            return False

        for file in files:
            file_path = os.path.join(self.output_folder, file)
            os.remove(file_path)

        print(f"Se eliminaron {len(files)} archivos de audio.")
        return True

    @classmethod
    def get_recommended_voices(cls) -> dict:
        """
        Obtiene el diccionario de voces recomendadas.

        Returns:
            dict: Diccionario con alias y nombres de voces
        """
        return cls.RECOMMENDED_VOICES.copy()

    @classmethod
    def print_recommended_voices(cls):
        """
        Imprime las voces recomendadas disponibles.
        """
        print("🎙️  === VOCES RECOMENDADAS EN ESPAÑOL ===")
        print()

        for alias, voice_name in cls.RECOMMENDED_VOICES.items():
            gender = "Femenina" if "femenina" in alias else "Masculina"
            region = "España" if "españa" in alias else "Estados Unidos" if "estados_unidos" in alias else "General"
            print(f"📢 {alias}")
            print(f"   Voz: {voice_name}")
            print(f"   Género: {gender}")
            print(f"   Región: {region}")
            print()

    def change_voice(self, voice_name: str):
        """
        Cambia la voz del servicio.

        Args:
            voice_name (str): Nombre de la nueva voz
        """
        old_voice = self.voice_name

        # Si es un alias de voz recomendada, convertir al nombre real
        if voice_name in self.RECOMMENDED_VOICES:
            self.voice_name = self.RECOMMENDED_VOICES[voice_name]
        else:
            self.voice_name = voice_name

        print(f"Voz cambiada de '{old_voice}' a '{self.voice_name}'")


# --- Ejemplo de cómo probarlo ---
if __name__ == "__main__":
    # 1. Asegúrate de haber configurado tus credenciales de Google
    #    En tu terminal: export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/tu/archivo.json"

    # 2. Crea una instancia del servicio
    tts_service = TTSService()

    # 3. Define el texto que quieres convertir
    texto_para_convertir = "Hola, soy Polito, la tortuga seleccionadora de ESPOL. Dime, ¿qué es lo que más te apasiona en el mundo?"

    # 4. Llama a la función
    resultado = tts_service.synthesize_and_save(texto_para_convertir)

    if resultado:
        print(f"Archivo creado exitosamente: {resultado}")

    # Segunda prueba para verificar la secuencia de nombres
    otro_texto = "Muy interesante. Ahora cuéntame, ¿prefieres trabajar en equipo o disfrutas más resolviendo problemas por tu cuenta?"
    resultado2 = tts_service.synthesize_and_save(otro_texto)

    if resultado2:
        print(f"Segundo archivo creado: {resultado2}")

    # Mostrar todos los archivos generados
    archivos = tts_service.list_generated_files()
    print(f"Archivos generados: {archivos}")
