from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from weather_data import get_weather
from utils import weather_message, get_uv_advice
from chatbot import get_chatbot_response
from city_manager import TOP_CITIES
import auth

app = Flask(__name__)
app.secret_key = "weatherly_dev_key"

def get_bg_video(condition):
    if not condition:
        return "default.mp4"
        
    cond = condition.lower()
    if "fog" in cond or "ceață" in cond or "mist" in cond:
        return "fog.mp4"
    elif "senin" in cond or "clear" in cond or "soare" in cond or "însorit" in cond:
        return "sun.mp4"
    elif "rain" in cond or "ploaie" in cond or "drizzle" in cond:
        return "rain.mp4"
    elif "cloud" in cond or "noros" in cond or "acoperit" in cond:
        return "cloud.mp4"
    elif "snow" in cond or "zapada" in cond or "ninsori" in cond:
        return "snow.mp4"
    return "default.mp4"

@app.route("/")
def index_redirect():
    city = "Bucharest"
    weather_info = get_weather(city)
    bg_video = "default.mp4"
    
    if "error" not in weather_info:
        bg_video = get_bg_video(weather_info["condition"])
        message = weather_message(weather_info["temperature"], weather_info["condition"])
    else:
        message = "Bine ai venit! Caută un oraș pentru a vedea vremea."

    return render_template("index.html", 
                           weather=weather_info, 
                           city=city, 
                           message=message, 
                           bg_video=bg_video)

@app.route("/", methods=["POST"])
def home():
    city = request.form.get("city", "București")
    weather_info = get_weather(city)
    
    bg_video = "default.mp4" 
    
    if "error" not in weather_info:
        message = weather_message(weather_info["temperature"], weather_info["condition"])
        bg_video = get_bg_video(weather_info["condition"])
    else:
        message = weather_info["error"]
        
    return render_template("index.html", 
                           weather=weather_info, 
                           city=city, 
                           message=message, 
                           bg_video=bg_video)

@app.route("/about")
def about():
    return render_template("about_us.html", bg_video="default.mp4")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    response = get_chatbot_response(data.get("message", ""))
    return jsonify({"response": response})

@app.route("/more_details/<city>")
def more_details(city):
    w = get_weather(city)
    bg_video = get_bg_video(w.get("condition", ""))
    advice = get_uv_advice(w.get("uv", 0))
    return render_template("more_details.html", weather=w, city=city, uv_advice=advice, bg_video=bg_video)

@app.route("/popular_cities")
def popular_cities():
    # Adăugăm bg_video și aici pentru a păstra fundalul pe pagina cu lista de orașe
    return render_template("popular_cities.html", cities=TOP_CITIES, bg_video="default.mp4")

if __name__ == "__main__":
    app.run(debug=True)