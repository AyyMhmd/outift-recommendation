import requests
import json

url = "http://localhost:5000/api/recommend"
payload = {
    "lat": -6.2088,
    "lon": 106.8456,
    "gender": "Men",
    "season": "Summer",
    "usage": "Casual"
}
headers = {"Content-Type": "application/json"}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"FAILED to connect: {e}")
