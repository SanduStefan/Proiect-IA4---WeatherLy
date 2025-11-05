from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_TOKEN = "714bf56178b24ab6aef210524250511"
API_URL = "https://api.weatherapi.com/v1/current.json"

def weather_message(temp, condition):
    condition_lower = condition.lower()
    if "rain" in condition_lower or "ploaie" in condition_lower:
        return "Ia umbrela cu tine ☔"
    elif "snow" in condition_lower or "zăpadă" in condition_lower:
        return "Prea frig, pregătește sania!"
    elif temp > 30:
        return "Nu uita crema de soare!"
    elif temp > 20 and temp < 25:
        return "Vreme numai buna de purtat tricou!"
    elif temp > 20:
        return "O zi perfectă pentru plimbare!"
    elif temp >= 10:
        return "Temperatură plăcută, o zi frumoasă!"
    elif temp >0 and temp < 10:
        return "Este destul de frig, fii atent la îmbrăcăminte"
    else:
        return "Îmbracă-te bine, este frig afară!"

@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather_info = {}
    message = ""
    
    if request.method == "POST":
        city = request.form.get("city")
        
        try:
            response = requests.get(API_URL, params={"key": API_TOKEN, "q": city})
            data = response.json()

            weather_info = {
                "temperature": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "uv": data["current"]["uv"],
                "wind_kph": data["current"]["wind_kph"],
                "feelslike_c": data["current"]["feelslike_c"]
            }

            message = weather_message(weather_info["temperature"], weather_info["condition"])

        except Exception as e:
            weather_info = {"error": str(e)}
            message = "Nu s-au putut prelua datele pentru acest oraș."

    return render_template("index.html", weather=weather_info, city=city, message=message)

if __name__ == "__main__":
    app.run(debug=True)
