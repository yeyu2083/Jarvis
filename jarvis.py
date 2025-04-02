import pyttsx3
from decouple import config
import tempfile
import os
import platform

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

# Initialize text-to-speech engine based on platform
def init_engine():
    """Inicializa el motor de voz según la plataforma del sistema"""
    if platform.system() == 'Windows':
        engine = pyttsx3.init('sapi5')
    elif platform.system() == 'Darwin':  # macOS
        engine = pyttsx3.init('nsss')
    else:  # Linux
        engine = pyttsx3.init('espeak')
    return engine

engine = init_engine()

# setProperty es un metodo para el motor de voz

# Set Rate
engine.setProperty('rate', 190)
# Set Volumen
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#Conversion de Texto a voz

def speak(text):
    """Usado para decir cualquier texto que le sea entregado, utilizan la biblioteca pyttsx3 y los metodos say() para el texto y runandwait() para ejecutar el texto a voz"""
    
    engine.say(text)
    engine.runAndWait()

    # funcion para dar la bienvenida en tiempo real

from datetime import datetime

def greet_user():
    """Saluda al usuario de acuerdo al horario"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Buenos Dias {USERNAME}")
    elif (hour >= 12) and (hour <  16):
        speak(f"Buenas tardes {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Buenas Noches {USERNAME}")
    speak(f"Yo soy {BOTNAME}. ¿Cómo puedo ayudarle?")

#configuramos la informaciòn del usuario

"""Modulo speech_recognition como sr, recognizer es una clase para reconocer el audio, y microphone para el microfono, con source y escuchamos el audio con listen()"""

import speech_recognition as sr
from random import choice
from utils import opening_text

def take_user_input():
    """Toma las entradas del usuario, las reconoce por el mòdulo de voz, pause_threshold es la pausa para q no compile mientras hablamos, recognize ejecuta el reconocimiento de la voz usando la api de google"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-ES')
        if not 'Salir' in query or 'Alto' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Buenas noches señor, !cuídese!")
            else:
                speak("Tenga un buen dia!")
            exit()

    except Exception:
                speak("Lo siento , puede repetirlo?")
                query = 'None'
    return query

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
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(
            prefix=prefix,
            suffix=suffix,
            delete=False,
            mode='w'
        )
        
        # Escribir datos
        temp_file.write(str(data))
        temp_file.close()
        
        speak(f"Archivo temporal creado en {temp_file.name}")
        return temp_file.name
        
    except Exception as e:
        speak("Error al crear archivo temporal")
        print(f"Error: {str(e)}")
        return None

def delete_temp_file(filepath):
    """
    Elimina un archivo temporal.
    
    Args:
        filepath: Ruta del archivo a eliminar
    """
    try:
        os.remove(filepath)
        speak("Archivo temporal eliminado")
    except Exception as e:
        speak("Error al eliminar archivo temporal") 
        print(f"Error: {str(e)}")
