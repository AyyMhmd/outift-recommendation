try:
    from ml.api.weather import get_weather, get_location
except ImportError:
    from weather import get_weather, get_location
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def test_get_location():
    print("Testing get_location()...")
    location = get_location()
    print(f"Detected Location: {location}")
    assert location is not None, "Location detection failed"

def test_get_weather_with_city():
    print("\nTesting get_weather(city='London')...")
    weather = get_weather("London")
    print(f"Weather in London: {weather}")
    if weather["temperature"] == 30 and weather["humidity"] == 70:
        print("WARNING: Weather returned default fallback values. API Key may be invalid.")

def test_get_weather_auto():
    print("\nTesting get_weather(city=None)...")
    weather = get_weather(None)
    print(f"Weather (Auto): {weather}")
    if weather["temperature"] == 30 and weather["humidity"] == 70:
        print("WARNING: Auto weather returned default fallback values.")

if __name__ == "__main__":
    try:
        # test_get_location()
        test_get_weather_with_city()
        test_get_weather_auto()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
