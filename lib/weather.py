import requests
from datetime import datetime
from dateutil import tz
import time

def get_weather(weatherUrl):
    
    response = requests.get(weatherUrl)
    #response = requests.get('http://api.weatherapi.com/v1/forecast.json?key=b0c3591a2dc94f31a3713621210903&q=05403&days=1&aqi=no&alerts=no')
    weather_json_data = response.json() if response and response.status_code == 200 else None

    return weather_json_data