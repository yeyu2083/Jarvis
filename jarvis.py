import pyttsx3
from decouple import config

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

# modulo pyttsx3 con sapi5 (API) de vos de microsoft
engine = pyttsx3.init('sapi5')

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
