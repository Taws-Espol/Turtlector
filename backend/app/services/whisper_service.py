import os
from openai import OpenAI
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write
import time
import threading
import queue

def mostrar_instrucciones():
    """Muestra las instrucciones de control para el usuario."""
    print("\n" + "="*50)
    print("CONTROLES DE GRABACIÓN:")
    print("Presiona 'p' + Enter para PAUSAR/REANUDAR")
    print("Presiona 'q' + Enter para DETENER y transcribir")
    print("="*50)

def configurar_directorios():
    """Crea los directorios necesarios para las grabaciones y transcripciones."""
    os.makedirs("grabaciones", exist_ok=True)
    os.makedirs("transcripciones", exist_ok=True)


def grabar_audio_indefinido(nombre_archivo, fs=44100):
    """
    Graba audio indefinidamente hasta que el usuario lo detenga.
    :param nombre_archivo: Ruta donde guardar el archivo de audio
    :param fs: Frecuencia de muestreo (Hz)
    :return: True si la grabación fue exitosa, False en caso contrario
    """
    try:
        print(f"🔴 INICIANDO grabación...")
        mostrar_instrucciones()
        
        # Cola para comunicación entre hilos
        comando_queue = queue.Queue()
        grabacion_activa = threading.Event()
        detener_grabacion = threading.Event()
        
        grabacion_activa.set()  # Iniciar grabando
        
        # Hilo para capturar comandos del usuario
        def capturar_comandos():
            while not detener_grabacion.is_set():
                try:
                    comando = input().strip().lower()
                    comando_queue.put(comando)
                except:
                    break
        
        # Iniciar hilo de comandos
        hilo_comandos = threading.Thread(target=capturar_comandos, daemon=True)
        hilo_comandos.start()
        
        # Lista para almacenar chunks de audio
        chunks_audio = []
        chunk_duration = 1.0  # Grabar en chunks de 1 segundo
        chunk_frames = int(fs * chunk_duration)
        
        pausado = False
        
        while not detener_grabacion.is_set():
            # Verificar comandos del usuario
            try:
                comando = comando_queue.get_nowait()
                if comando == 'p':
                    pausado = not pausado
                    if pausado:
                        print("⏸️  PAUSADO - Presiona 'p' + Enter para reanudar")
                        grabacion_activa.clear()
                    else:
                        print("▶️  REANUDANDO grabación...")
                        grabacion_activa.set()
                elif comando == 'q':
                    print("🛑 DETENIENDO grabación...")
                    detener_grabacion.set()
                    break
            except queue.Empty:
                pass
            
            # Si no está pausado, grabar chunk
            if not pausado and not detener_grabacion.is_set():
                try:
                    # Grabar chunk de audio
                    chunk = sd.rec(chunk_frames, samplerate=fs, channels=1, dtype='int16')
                    sd.wait()  # Esperar a que termine el chunk
                    chunks_audio.append(chunk)
                except:
                    break
            else:
                time.sleep(0.1)  # Pequeña pausa si está pausado
        
        # Guardar todo el audio grabado
        if chunks_audio:
            import numpy as np
            audio_completo = np.concatenate(chunks_audio, axis=0)
            write(nombre_archivo, fs, audio_completo)
            print(f"✅ Audio guardado en '{nombre_archivo}'")
            return True
        else:
            print("❌ No se grabó audio")
            return False
            
    except Exception as e:
        print(f"❌ Error al grabar audio: {e}")
        return False
    
def transcribir_audio(archivo_audio, archivo_transcripcion):
    """
    Transcribe un archivo de audio usando la API de Whisper.
    :param archivo_audio: Ruta del archivo de audio a transcribir
    :param archivo_transcripcion: Ruta donde guardar la transcripción
    :return: True si la transcripción fue exitosa, False en caso contrario
    """
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    try:
        with open(archivo_audio, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            with open(archivo_transcripcion, "w", encoding='utf-8') as trans_file:
                trans_file.write(transcription)
            print(f"✅ Transcripción guardada en '{archivo_transcripcion}'")
            return True
    except Exception as e:
        print(f"❌ Error en la transcripción: {e}")
        return False

def generar_nombres_archivos(contador):
    """
    Genera los nombres de archivos para audio y transcripción.
    :param contador: Número del archivo
    :return: Tupla con (nombre_audio, nombre_transcripcion)
    """
    nombre_audio = f"grabaciones/audio_{contador}.wav"
    nombre_transcripcion = f"transcripciones/transcripcion_{contador}.txt"
    return nombre_audio, nombre_transcripcion

def grabar_y_transcribir_audio(fs=44100):
    """
    Función principal que maneja la grabación indefinida y transcripción.
    :param fs: Frecuencia de muestreo (Hz)
    """
    contador = 1
    configurar_directorios()
    
    try:
        while True:
            nombre_audio, nombre_transcripcion = generar_nombres_archivos(contador)
            print(f"\n🎙️  === SESIÓN DE GRABACIÓN {contador} ===")
            
            # Grabar audio indefinidamente
            if grabar_audio_indefinido(nombre_audio, fs):
                print(f"\n📝 Iniciando transcripción...")
                transcribir_audio(nombre_audio, nombre_transcripcion)
                
                # Preguntar si quiere hacer otra grabación
                print(f"\n¿Deseas hacer otra grabación? (s/n): ", end="")
                respuesta = input().strip().lower()
                if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                    print("👋 ¡Hasta luego!")
                    break
                    
                contador += 1
            else:
                print("❌ Error en la grabación. Intentando nuevamente...")
                
    except KeyboardInterrupt:
        print("\n🛑 Programa interrumpido por el usuario.")
        return