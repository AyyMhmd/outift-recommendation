import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return data["city"]
        else:
            print("Failed to detect location, defaulting to Jakarta.")
            return "Jakarta"
    except Exception as e:
        print(f"Error detecting location: {e}")
        return "Jakarta"


def get_weather(city: str):
    if not city:
        city = get_location()

    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        return {"temperature": data["main"]["temp"], "humidity": data["main"]["humidity"]}
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return {"temperature": 30, "humidity": 70}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"temperature": 30, "humidity": 70}
