from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from auth import db, User
from weather_data import get_weather
from utils import weather_message, get_uv_advice
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
    if any(x in cond for x in ["fog", "ceață", "mist"]): return "fog.mp4"
    if any(x in cond for x in ["senin", "clear", "soare", "sunny"]): return "sun.mp4"
    if any(x in cond for x in ["rain", "ploaie", "drizzle", "burniță"]): return "rain.mp4"
    if any(x in cond for x in ["cloud", "nor", "acoperit"]): return "cloud.mp4"
    if any(x in cond for x in ["snow", "zapada", "ninsori"]): return "snow.mp4"
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
    return render_template("index.html", weather=w, city=city, message=msg, bg_video=bg)

# RUTA CORECTATĂ PENTRU DETALII
@app.route("/more_details/<city>")
def more_details(city):
    w = get_weather(city)
    if "error" in w:
        return redirect(url_for('index'))
    
    bg = get_bg_video(w.get("condition", ""))
    advice = get_uv_advice(w.get("uv", 0))
    # Simulare istoric temperaturi pentru grafic
    temp_history = [w['temperature']-2, w['temperature']-1, w['temperature']+2, w['temperature']+3, w['temperature']+1, w['temperature']-1, w['temperature']]
    
    return render_template("more_details.html", 
                           weather=w, 
                           city=city, 
                           uv_advice=advice, 
                           bg_video=bg, 
                           temp_history=temp_history)

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