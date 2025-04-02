import datetime
import platform
import os

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
        else:
            speak("No entiendo ese comando. ¿Puedes repetirlo?")