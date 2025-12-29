import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str):
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    return {"temperature": data["main"]["temp"], "humidity": data["main"]["humidity"]}
