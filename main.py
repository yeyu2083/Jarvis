import  requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message, get_trending_movies, get_weather_report,search_spotify, play_on_spotify
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from jarvis import speak, greet_user, take_user_input
from pprint import pprint

if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if'abrir bloc de notas' in query:
            open_notepad()

        elif 'abrir discord' in query:
            open_discord()

        elif 'abrir simbolo del sistema' in query or 'open cmd' in query:
            open_cmd()
        
        elif 'abrir camera' in query:
            open_camera()
        
        elif 'abrir calculadora' in query:
            open_calculator()
        
        elif 'ip_adress' in query:
            ip_address = find_my_ip()
            speak(f'Su Direccion IP es {ip_address}.\n para su comodidad la he mostrado en consola')
            print(f'Tu direccion  IP es {ip_address}')
        
        elif 'wikipedia' in query:
            speak('¿Qué quiere buscar en Wikipedia, señor?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"De acuerdo con Wikipedia, {results}")
            speak('Para su comodidad, mostrare en pantalla los resultados, señor')
            print(results)
        
        elif 'youtube' in query:
            speak('¿Que desea ver en YouTube, señor?')
            video = take_user_input().lower()
            play_on_youtube(video)
        
        elif 'buscar en google' in query:
            speak('¿Qué desea buscar en Google, señor?')
            query = take_user_input().lower()
            search_on_google(query)
        elif 'escuchar en spotify' in query:
            speak('¿Qué canción desea buscar en Spotify, señor?')
            query = take_user_input().lower()
            song = query.replace(" ", "%20")
            search_spotify()

        elif "enviar mensaje de WhatsApp" in query:
            speak('¿A qué número debería enviar el mensaje señor?, por favor, digítelo en la consola: ')
            number = input("Ingrese el número: ")
            speak("¿Cúal es el mensaje, señor?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("El mensaje ha sido enviado, señor.")

        elif "enviar un email" in query:
            speak("¿A qué dirección de correo la envío, señor? Por favor, ingresela en la consola: ")
            receiver_address = input("Ingrese la dirección de correo electrónico: ")
            speak("¿Cuál es el asunto, señor?")
            subject = take_user_input().capitalize()
            speak("¿Cuál es el mensaje, señor?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("El correo ha sido enviado, señor.")
            else:
                speak("Algo ha salido mal mientras estaba enviando el correo, por favor revise el registro de errores, señor.")
        
        elif 'chiste' in query:
            speak(f"Espero le guste este, señor.")
            joke = get_random_joke()
            speak(joke)
            speak("Para su goce, se lo mostraré en la pantalla, señor.")
            pprint(joke)

        elif "consejo" in query:
            speak(f"Acá hay un consejo para usted, señor.")
            advice = get_random_advice()
            speak(advice)
            speak("Para su disfrute, lo estoy mostrando en la pantalla, señor.")
            pprint(advice)

        elif "peliculas en tendencia" in query:
            speak(f"Algunas de las películas en tendencia son: {get_trending_movies()}")
            speak("Para su mejor comprensión, están en la pantalla, señor.")
            print(*get_trending_movies(), sep='\n')

        elif 'noticias' in query:
            speak(f"Estoy leyendo los últimos titulares de las noticias, señor.")
            speak(get_latest_news())
            speak("Para su comodidad, las mostraré en la pantalla, señor.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Obteniendo el reporte del clima en su ciudad {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"La temperatura actual es {temperature}, pero se siente más como {feels_like}")
            speak(f"Además, el reporte menciona acerca de {weather}")
            speak("Para mejor información, se la mostraré en la pantalla, señor.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")