from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_TOKEN = "714bf56178b24ab6aef210524250511"
API_URL = "https://api.weatherapi.com/v1/current.json"

@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather_info = {}
    
    if request.method == "POST":
        city = request.form.get("city")
        
        try:
            response = requests.get(API_URL, params={
                "key": API_TOKEN,
                "q": city
            })
            data = response.json()

            if "error" in data:
                weather_info = {"error": data["error"]["message"]}
            else:
                current = data["current"]
                weather_info = {
                    "temperature": current["temp_c"],
                    "condition": current["condition"]["text"],
                    "humidity": current["humidity"],
                    "uv": current.get("uv"),
                    "wind_kph": current.get("wind_kph"),
                    "feelslike_c": current.get("feelslike_c")
                }

        except Exception as e:
            weather_info = {"error": "A apărut o eroare la conectarea cu API-ul: " + str(e)}

    return render_template("index.html", weather=weather_info, city=city)

if __name__ == "__main__":
    app.run(debug=True)
