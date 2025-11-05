from flask import Flask, render_template
import requests

app = Flask(__name__)

API_TOKEN = "714bf56178b24ab6aef210524250511"
API_URL = "https://api.weatherapi.com/v1/current.json"

@app.route("/")
def home():
    city = "Bucharest"
    try:
        response = requests.get(API_URL, params={
            "key": API_TOKEN,
            "q": city
        })
        data = response.json()

        # Extragem cele 3 date principale
        weather_info = {
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"]
        }

    except Exception as e:
        weather_info = {"error": str(e)}

    return render_template("index.html", weather=weather_info, city=city)

if __name__ == "__main__":
    app.run(debug=True)
