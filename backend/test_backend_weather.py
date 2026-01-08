import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.app import get_weather_data, get_location
except ImportError:
    # Try local import if running from backend dir directly
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from app import get_weather_data, get_location

def test_backend_location():
    print("Testing backend get_location()...")
    loc = get_location()
    print(f"Detected Location: {loc}")
    assert loc is not None

def test_backend_weather_auto():
    print("\nTesting backend get_weather_data(city=None)...")
    data = get_weather_data(None)
    print(f"Weather Data: {data}")
    
    # Check if we got valid data or fallback
    if data["temperature"] == 28 and data["humidity"] == 75:
        print("WARNING: Returned default fallback values. (Likely invalid API Key)")
    else:
        print("SUCCESS: Retrieved specific weather data.")
        
    assert "temperature" in data
    assert "city" in data

if __name__ == "__main__":
    try:
        test_backend_location()
        test_backend_weather_auto()
        print("\nBackend weather tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
