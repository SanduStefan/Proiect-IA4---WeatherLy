from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from weather_data import get_weather
from utils import weather_message, get_uv_advice
from chatbot import get_chatbot_response
from city_manager import TOP_CITIES
from flask_login import LoginManager, login_required, current_user
import auth

app = Flask(__name__)
app.secret_key = "weatherly_dev_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Integrare Auth Coleg
auth.init_auth(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return auth.User.query.get(int(user_id))

def get_bg_video(condition):
    if not condition: return "default.mp4"
    cond = condition.lower()
    if any(x in cond for x in ["fog", "ceață", "mist"]): return "fog.mp4"
    if any(x in cond for x in ["senin", "clear", "soare", "însorit"]): return "sun.mp4"
    if any(x in cond for x in ["rain", "ploaie", "drizzle"]): return "rain.mp4"
    if any(x in cond for x in ["cloud", "noros", "acoperit"]): return "cloud.mp4"
    if any(x in cond for x in ["snow", "zapada", "ninsori"]): return "snow.mp4"
    return "default.mp4"

@app.route("/")
def index_redirect():
    city = "Bucharest"
    weather_info = get_weather(city)
    bg_video = get_bg_video(weather_info.get("condition"))
    message = weather_message(weather_info.get("temperature", 0), weather_info.get("condition", ""))
    return render_template("index.html", weather=weather_info, city=city, message=message, bg_video=bg_video)

@app.route("/", methods=["POST"])
def home():
    city = request.form.get("city", "București")
    weather_info = get_weather(city)
    bg_video = get_bg_video(weather_info.get("condition"))
    message = weather_message(weather_info.get("temperature", 0), weather_info.get("condition", "")) if "error" not in weather_info else weather_info["error"]
    return render_template("index.html", weather=weather_info, city=city, message=message, bg_video=bg_video)

# Rute Login Coleg cu Designul Tau
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = auth.User.query.filter_by(username=request.form.get("username")).first()
        if user and auth.check_password_hash(user.password, request.form.get("password")):
            from flask_login import login_user
            login_user(user)
            return redirect(url_for("index_redirect"))
    return render_template("login.html", bg_video="city.mp4")

@app.route("/metric_data")
@login_required
def metric_data():
    city = "Bucharest"
    w = get_weather(city)
    return render_template("metric_data.html", weather=w, city=city, bg_video="default.mp4")

@app.route("/about")
def about(): return render_template("about_us.html", bg_video="default.mp4")

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
def popular_cities(): return render_template("popular_cities.html", cities=TOP_CITIES, bg_video="city.mp4")

if __name__ == "__main__":
    app.run(debug=True)