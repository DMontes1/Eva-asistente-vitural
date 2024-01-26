import webbrowser
import pyautogui
import pyttsx3
import time
import speech_recognition as sr
import requests
import matplotlib.pyplot as plt

# Reemplaza 'TU_CLAVE_DE_API' con tu clave de OpenWeatherMap
API_KEY_CLIMA = '027c24f4f1521ec1bcd0bca7d682d265'
# Reemplaza 'TU_CLAVE_DE_API_NOTICIAS' con tu clave de News API
API_KEY_NOTICIAS = 'a498a417379c4271823b97185a0875d0'

# Función para abrir el explorador y dirigirse a YouTube
def abrir_explorador():
    url = "https://www.youtube.com"
    webbrowser.open(url)

# Función para reproducir una canción en YouTube
def reproducir_cancion(cancion):
    url = f"https://www.youtube.com/results?search_query={cancion}"
    webbrowser.open(url)

    # Espera un momento para que la página se cargue
    time.sleep(3)

    # Utiliza pyautogui para hacer clic en la posición del primer resultado
    pyautogui.click(x=756, y=311)  # Ajusta las coordenadas según tu pantalla

# Función para la síntesis de voz
def hablar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

# Función para reconocimiento de voz
def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Esperando activación... Di 'eva' para comenzar.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Reconociendo activación...")
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Texto reconocido: {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error en la solicitud de reconocimiento de voz: {e}")
        return ""

# Función para obtener el clima
def obtener_clima(ciudad):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': ciudad,
        'appid': API_KEY_CLIMA,
        'lang': 'es',  # Configura el lenguaje de la respuesta
        'units': 'metric'  # Configura las unidades métricas para temperatura en Celsius
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        clima = data['weather'][0]['description']
        temperatura = data['main']['temp']
        hablar(f"El clima en {ciudad} es {clima} y la temperatura es de {temperatura} grados Celsius.")
    else:
        hablar(f"No se pudo obtener la información del clima para {ciudad}.")

# Función para obtener noticias
def obtener_noticias():
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': API_KEY_NOTICIAS,
        'country': 'mx',  # Reemplaza 'tu_pais' con el código de país deseado (por ejemplo, 'us' para Estados Unidos)
        'pageSize': 3  # Número de noticias a obtener
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        noticias = data['articles']
        for idx, noticia in enumerate(noticias, start=1):
            titulo = noticia['title']
            hablar(f"Noticia {idx}: {titulo}")
    else:
        hablar("No se pudo obtener la información de noticias.")

# Función para obtener datos de criptomonedas y mostrarlos en una gráfica
def mostrar_grafico_cripto():
    base_url = "https://api.coingecko.com/api/v3/simple/price"
    cripto_monedas = ["bitcoin", "ethereum", "ripple"]  # Puedes agregar más criptomonedas según tus preferencias

    precios = {}

    for cripto in cripto_monedas:
        params = {
            'ids': cripto,
            'vs_currencies': 'usd'
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            precios[cripto] = data[cripto]['usd']
        else:
            precios[cripto] = None

    # Crear una gráfica de barras
    plt.figure(figsize=(10, 6))

    # Crear barras para cada criptomoneda
    for i, (cripto, precio) in enumerate(precios.items()):
        if precio is not None:
            plt.bar(i, precio, label=cripto, color='blue')

    # Agregar etiquetas y título a la gráfica
    plt.xlabel('Criptomonedas')
    plt.ylabel('Precio en USD')
    plt.title('Precios de Criptomonedas')

    # Agregar etiquetas de criptomonedas en el medio de cada barra
    plt.xticks(range(len(cripto_monedas)), [f'{cripto}\n${precio}' for cripto, precio in precios.items()])

    # Mostrar leyenda
    plt.legend()

    # Mostrar la gráfica
    plt.show()

if __name__ == "__main__":
    while True:
        activacion = escuchar()

        if "eva" in activacion:
            hablar("¡Hola! ¿En qué puedo ayudarte?")

            print("Puedes decir 'abrir explorador', 'reproducir música', 'clima', 'noticias', 'cripto' o 'salir'")
            comando = escuchar()

            comandos_reproducir_musica = ["reproducir música", "escuchar música", "pon música", "pon musica", "quiero escuchar algo"]
            comandos_clima = ["clima", "pronóstico", "temperatura"]
            comandos_noticias = ["noticias", "últimas noticias"]
            comandos_cripto = ["cripto", "criptomonedas", "crypto", "krypto", "kripto"]

            if any(accion in comando for accion in comandos_reproducir_musica):
                hablar("¿Cuál es el nombre de la canción?")
                cancion = escuchar()
                hablar(f"Reproduciendo {cancion} en YouTube.")
                reproducir_cancion(cancion)
            elif any(accion in comando for accion in comandos_clima):
                hablar("¿De qué ciudad quieres conocer el clima?")
                ciudad = escuchar()
                obtener_clima(ciudad)
            elif any(accion in comando for accion in comandos_noticias):
                hablar("Obteniendo las últimas noticias.")
                obtener_noticias()
            elif any(accion in comando for accion in comandos_cripto):
                hablar("Obteniendo datos de criptomonedas.")
                mostrar_grafico_cripto()
            elif "abrir explorador" in comando:
                hablar("Abriendo el explorador web.")
                abrir_explorador()
            elif "salir" in comando:
                hablar("Hasta luego.")
                break
            else:
                hablar("No se reconoció ningún comando válido. Intenta de nuevo.")
        else:
            print("Palabra clave no reconocida. Intenta de nuevo.")
