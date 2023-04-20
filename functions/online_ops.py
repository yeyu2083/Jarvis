import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
import webbrowser as web
from decouple import config
from jarvis import speak, take_user_input
import pyautogui
from time import sleep


client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
flag = 0
#sPOTYFI
author = ''
song = ''


   
  
def play_on_spotify():
  global song
  speak("que cancion desea escuchar?")
  query = take_user_input()
  if "" in query:
      song = query.upper()
      search_spotify()
  else:
      pass


def search_spotify():
    global flag
    global song
    
    if flag == 0:
        song = song.replace(" ", "%20")
        web.open(f"spotify:search:{song}")
        sleep(5)
        for i in range(28):
            pyautogui.press("tab")
        pyautogui.press("enter")

search_spotify()


{
  "ip": "117.214.111.199"
}
#encontrar el ip
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

#buscar en wikipedia
"""dentro de wikipedia, tenemos summary, q acepta una variable query como elemento, podemos indicar el num de oraciones requeridas"""
def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

#para mostrar youtube con pywhatkit(usamos la variable kit q definimos)
def play_on_youtube(video):
    kit.playonyt(video)

#busqueda en google, con pywhatkit y el comando search
def search_on_google(query):
    kit.search(query)

#para enviar mensajes por whatsapp usamos pywhatkit, acepta dos elem , n y msg
def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+54 9{number}", message)

#configuracion para email

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

"""la funcion tiene 3 argumentos, tenemos el objeto emailmessage,q almacena los detalles del c.electronico, se crea una conexion con el servidor SMTP de gmail en el puerto 587, con la funcion smtplib.SMTP, se llama al metodo s.starttls() para la conexion, s.login() para q ingrese el usuario , s.send_message para el cuerpo y se cierra con s.close()"""

def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False
    


#configuramos la NEWAPI

NEWS_API_KEY = config("NEWS_API_KEY")

def get_latest_news():
    news_headlines = []
    res = requests.get(
         f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

#configuracion de la APIWEATHER

OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")

def get_weather_report(city):
    res = requests.get(  
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}°C", f"{feels_like}°C"


#configuramos la APi de las peliculas

TMDB_API_KEY = config("TMDB_API_KEY")

def get_trending_movies():
    trending_movies = []
    res = requests.get(
         f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

#funcion chistes

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

#funcion para obtener chistes al azar

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip'] ['advice']

