from TTS.api import TTS
import pygame
import time

def init_tts_model(model_name="tts_models/es/css10/vits"):
    """
    Inicializa el modelo de TTS.
    """
    tts = TTS(model_name, progress_bar=True, gpu=False)
    return tts
/
def convert_text_to_speech(tts, text, output_file="temp.wav"):
    """
    Convierte un texto a voz y guarda el archivo de audio.
    """
    tts.tts_to_file(text=text, file_path=output_file)
    print(f"Conversión de texto a voz completada. Archivo guardado como '{output_file}'")

def play_audio(audio_file="temp.wav"):
    """
    Reproduce el archivo de audio generado.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    print("Reproducción finalizada")

def text_to_speech(text, model_name="tts_models/es/css10/vits", output_file="temp.wav"):
    """
    Función principal para convertir texto en voz y reproducirlo.
    """
    # Inicializa el modelo TTS
    tts = init_tts_model(model_name)

    # Convierte el texto a voz y guarda el archivo
    convert_text_to_speech(tts, text, output_file)

    # Reproduce el archivo de audio generado
    play_audio(output_file)
