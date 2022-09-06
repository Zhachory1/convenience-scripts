# Weather script to get weather from a search query

from absl import app 
from absl import flags 
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import os
import requests as req
import pprint

FLAGS = flags.FLAGS

flags.DEFINE_string("query", "", "Location query to get weather for")

def deg_to_cardinal(degrees):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    ix = round(degrees / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

class WeatherInterface:
    def __init__(self, key):
        self.key = key
        self.api_url = f"http://api.openweathermap.org/data/2.5/weather?"
    
    def get_weather(self, loc):
        # Set API
        params = f"q={loc}&appid={self.key}"
        
        # Get the response from the API
        url = self.api_url + params
        response = req.get(url)
        weather = response.json()
        # Fetch Weather
        print(f"Weather for {weather['name']}, {weather['sys']['country']}:")
        temp = int(weather['main']['temp'] - 273.15)
        print("Temperature:", temp, "Celsius")
        temp_max = int(weather['main']['temp_max'] - 273.15)
        temp_min = int(weather['main']['temp_min'] - 273.15)
        print(f"Highs and lows: {temp_max}-{temp_min} Celsius")
        humidity = weather['main']['humidity']
        print("Humidity:", humidity, "%")
        wind = weather['wind']['speed']
        dir = deg_to_cardinal(weather['wind']['deg'])
        print(f"Wind speed: {wind} m/s {dir}")
    

def main(argv):
    load_dotenv()
    weather = WeatherInterface(os.getenv('WEATHER_API_KEY'))
    weather.get_weather(FLAGS.query)

if __name__ == "__main__":
    app.run(main)    