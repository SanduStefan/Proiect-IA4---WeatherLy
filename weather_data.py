import requests

API_TOKEN = "714bf56178b24ab6aef210524250511"
API_URL = "https://api.weatherapi.com/v1/current.json"

def get_weather(city):
    try:
        response = requests.get(API_URL, params={"key": API_TOKEN, "q": city, "lang": "ro"})
        data = response.json()
        if "error" in data: return {"error": "Orașul nu a fost găsit."}
        
        return {
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "uv": data["current"]["uv"],
            "wind_kph": data["current"]["wind_kph"],
            "feelslike_c": data["current"]["feelslike_c"],
            "pressure_mb": data["current"]["pressure_mb"],
            "precip_mm": data["current"]["precip_mm"],
            "visibility_km": data["current"]["vis_km"],
            "icon": data["current"]["condition"]["icon"]
        }
    except:
        return {"error": "Eroare de conexiune la API."}