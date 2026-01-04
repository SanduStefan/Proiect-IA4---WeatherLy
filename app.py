from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from auth import db, User
from weather_data import get_weather
from utils import weather_message, get_uv_advice, get_continent
from chatbot import get_chatbot_response
from city_manager import DESTINATIONS, TOP_CITIES

app = Flask(__name__)
app.secret_key = "weatherly_secret_key_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

def get_bg_video(condition):
    cond = condition.lower() if condition else ""
    if any(x in cond for x in ["fog", "ceață", "mist", "vizibilitate"]): return "fog.mp4"
    if any(x in cond for x in ["soare", "sunny", "însorit", "canicula"]): return "sun.mp4"
    if any(x in cond for x in ["senin", "clear", "cer", "clar"]): return "clear.mp4"
    if any(x in cond for x in ["rain", "ploaie", "drizzle", "burniță", "ploi", "furtuni"]): return "rain.mp4"
    if any(x in cond for x in ["cloud", "nor", "nori", "acoperit", "înnorat"]): return "cloud.mp4"
    if any(x in cond for x in ["snow", "zapada", "ninsori", "lapoviță", "ninsoare"]): return "snow.mp4"
    return "default.mp4"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
    else:
        city = current_user.favorite_city if current_user.is_authenticated else "Bucharest"

    w = get_weather(city)
    bg = get_bg_video(w.get("condition", ""))

    msg = weather_message(w.get("temperature", 20), w.get("condition", "")) if "error" not in w else w.get("error")

    continent = None
    if w and "lat" in w and "lon" in w and w["lat"] is not None and w["lon"] is not None:
        continent = get_continent(w["lat"], w["lon"])

    return render_template(
        "index.html",
        weather=w,
        city=city,
        message=msg,
        bg_video=bg,
        continent=continent
    )

@app.route("/more_details/<city>")
def more_details(city):
    w = get_weather(city)
    if "error" in w:
        return redirect(url_for('index'))

  
    continent = get_continent(w.get("lat"), w.get("lon")) if w.get("lat") and w.get("lon") else None

    bg = get_bg_video(w.get("condition", ""))
    advice = get_uv_advice(w.get("uv", 0))

    temp_history = [
        w["temperature"] - 2,
        w["temperature"] - 1,
        w["temperature"],
        w["temperature"] + 1,
        w["temperature"] + 2,
        w["temperature"] + 1,
        w["temperature"]
    ]

    daily_min = [w.get("temp_min", w["temperature"] - 3)]
    daily_max = [w.get("temp_max", w["temperature"] + 3)]
    hour_labels = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]

    hourly_temps = [
        w["temperature"] - 2,
        w["temperature"] - 1,
        w["temperature"],
        w["temperature"] + 1,
        w["temperature"] + 2,
        w["temperature"] + 1,
        w["temperature"],
        w["temperature"] - 1
    ]

    hourly_feelslike = [
        w.get("feelslike_c", w["temperature"]) - 2,
        w.get("feelslike_c", w["temperature"]) - 1,
        w.get("feelslike_c", w["temperature"]),
        w.get("feelslike_c", w["temperature"]) + 1,
        w.get("feelslike_c", w["temperature"]) + 2,
        w.get("feelslike_c", w["temperature"]) + 1,
        w.get("feelslike_c", w["temperature"]),
        w.get("feelslike_c", w["temperature"]) - 1
    ]

    hourly_wind = [
        w["wind_kph"] - 2,
        w["wind_kph"],
        w["wind_kph"] + 1,
        w["wind_kph"] + 2,
        w["wind_kph"],
        w["wind_kph"] - 1,
        w["wind_kph"] - 2,
        w["wind_kph"]
    ]

    hourly_humidity = [w["humidity"]] * 8
    hourly_precip = [0, 0, 0.2, 0.5, 0.3, 0, 0, 0]

    return render_template(
        "more_details.html",
        weather=w,
        city=city,
        continent=continent,
        uv_advice=advice,
        bg_video=bg,
        temp_history=temp_history,
        daily_min=daily_min,
        daily_max=daily_max,
        hour_labels=hour_labels,
        hourly_temps=hourly_temps,
        hourly_feelslike=hourly_feelslike,
        hourly_wind=hourly_wind,
        hourly_humidity=hourly_humidity,
        hourly_precip=hourly_precip
    )

@app.route("/popular_cities")
def popular_cities():
    regions = ["Europa", "Asia", "America", "Africa & Altele"]
    categorized = {}
    for r in regions:
        if r == "Africa & Altele":
            cities = [d["name"] for d in DESTINATIONS if d.get("region") not in ["Europa", "Asia", "America"]]
        else:
            cities = [d["name"] for d in DESTINATIONS if d.get("region") == r]
        if cities: categorized[r] = sorted(cities)
    return render_template("popular_cities.html", categorized=categorized, bg_video="city.mp4")

@app.route("/minigame")
def minigame():
    return render_template("minigame.html", bg_video="games.mp4")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        current_user.favorite_city = request.form.get("fav_city")
        current_user.other_cities = request.form.get("other_cities")
        current_user.fav_destinations = request.form.get("fav_destinations")
        current_user.interests = request.form.get("interests")
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("settings.html", bg_video="login.mp4")


@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    profile = {"interests": current_user.interests} if current_user.is_authenticated else {}
    current_city = data.get("city", "")
    user_msg = data.get("message", "")
    full_prompt = f"Sunt în {current_city}. {user_msg}" if current_city else user_msg
    return jsonify({"response": get_chatbot_response(full_prompt, user_profile=profile)})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Utilizator existent", bg_video="default.mp4")
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw, favorite_city="Bucharest")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("register.html", bg_video="login.mp4")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html", bg_video="login.mp4")

@app.route("/about")
def about():
    return render_template("about_us.html", bg_video="default.mp4")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)