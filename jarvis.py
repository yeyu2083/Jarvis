import datetime
import platform
import os
import tempfile
import hashlib
from pathlib import Path

# Intentar importar las dependencias de audio, pero no fallar si no están disponibles
AUDIO_ENABLED = False
try:
    import speech_recognition as sr
    import pyttsx3
    AUDIO_ENABLED = True
except ImportError:
    print("Módulos de audio no disponibles. Funcionando en modo texto.")

# Configuración
from decouple import config
USERNAME = config('USER', default='Yeyu')
BOTNAME = config('BOTNAME', default='Jarvis')

# Inicializar sistema de voz si está disponible
engine = None
if AUDIO_ENABLED:
    try:
        if platform.system() == 'Windows':
            engine = pyttsx3.init('sapi5')
        elif platform.system() == 'Darwin':  # macOS
            engine = pyttsx3.init('nsss')
        else:  # Linux
            engine = pyttsx3.init('espeak')
        
        # Configurar velocidad y voz
        engine.setProperty('rate', 190)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
    except Exception as e:
        print(f"Error al inicializar el motor de voz: {e}")
        AUDIO_ENABLED = False

def speak(text):
    """
    Función para que el asistente hable o muestre texto
    """
    if AUDIO_ENABLED and engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error al hablar: {e}")
            print(f"{BOTNAME}: {text}")
    else:
        print(f"{BOTNAME}: {text}")

def greet_user():
    """
    Función para saludar al usuario según la hora del día
    """
    hour = datetime.datetime.now().hour
    
    if 6 <= hour < 12:
        speak(f"Buenos Días {USERNAME}")
    elif 12 <= hour < 18:
        speak(f"Buenas Tardes {USERNAME}")
    else:
        speak(f"Buenas Noches {USERNAME}")
    
    speak(f"Yo soy {BOTNAME}. ¿Cómo puedo ayudarle?")

def take_user_input():
    """
    Función para tomar entrada del usuario, ya sea por voz o texto
    """
    if AUDIO_ENABLED:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Escuchando...")
                recognizer.pause_threshold = 1
                audio = recognizer.listen(source)
            
            try:
                print("Reconociendo...")
                query = recognizer.recognize_google(audio, language='es-ES')
                print(f"Usuario: {query}")
                return query
            except Exception as e:
                print(f"Error en reconocimiento: {e}")
                return "None"
        except Exception as e:
            print(f"Error al acceder al micrófono: {e}")
            # Caer al modo texto si hay un error con el audio
            return input("Escriba su comando: ")
    else:
        # Modo texto cuando el audio no está disponible
        return input(f"{USERNAME}: ")

def save_temp_file(data, prefix="jarvis_", suffix=".tmp"):
    """
    Guarda datos en un archivo temporal y retorna la ruta del archivo.
    
    Args:
        data: Datos a guardar en el archivo
        prefix: Prefijo del nombre del archivo temporal
        suffix: Extensión del archivo temporal
    
    Returns:
        str: Ruta del archivo temporal creado
    """
    try:
        with tempfile.NamedTemporaryFile(
            prefix=prefix,
            suffix=suffix,
            delete=False,
            mode='w',
            encoding='utf-8'
        ) as temp_file:
            temp_file.write(str(data))
            speak(f"Archivo temporal creado en {temp_file.name}")
            return temp_file.name
    except Exception as e:
        speak(f"Error al crear archivo temporal: {str(e)}")
        return None

def detect_duplicate_content(directory="."):
    """
    Detecta contenido duplicado en archivos de texto.
    
    Args:
        directory: Directorio a analizar
    
    Returns:
        dict: Diccionario de archivos con contenido duplicado
    """
    hash_dict = {}
    duplicates = {}
    
    try:
        for file_path in Path(directory).rglob("*.txt"):
            with open(file_path, 'rb') as f:
                content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
                
                if file_hash in hash_dict:
                    if file_hash not in duplicates:
                        duplicates[file_hash] = [hash_dict[file_hash]]
                    duplicates[file_hash].append(str(file_path))
                else:
                    hash_dict[file_hash] = str(file_path)
        
        if duplicates:
            speak("Se encontraron archivos duplicados:")
            for hash_value, files in duplicates.items():
                speak(f"Archivos duplicados: {', '.join(files)}")
        else:
            speak("No se encontraron archivos duplicados")
            
        return duplicates
    except Exception as e:
        speak(f"Error al buscar duplicados: {str(e)}")
        return {}

# Ejemplo de ejecución
if __name__ == "__main__":
    greet_user()
    
    while True:
        query = take_user_input()
        if query.lower() == 'salir' or query.lower() == 'exit':
            speak("Hasta luego")
            break
        
        # Procesar la consulta del usuario
        if 'hola' in query.lower():
            speak("Hola, ¿en qué puedo ayudarte?")
        elif 'hora' in query.lower():
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"La hora actual es {current_time}")
        elif 'fecha' in query.lower():
            date = datetime.datetime.now().strftime("%d/%m/%Y")
            speak(f"La fecha de hoy es {date}")
        elif 'guardar nota' in query.lower():
            speak("¿Qué contenido quieres guardar?")
            content = take_user_input()
            temp_file = save_temp_file(content, prefix="jarvis_nota_", suffix=".txt")
            if temp_file:
                speak(f"Nota guardada en {temp_file}")
                
        elif 'buscar duplicados' in query.lower():
            speak("Buscando archivos duplicados...")
            detect_duplicate_content()
            
        else:
            speak("No entiendo ese comando. ¿Puedes repetirlo?")