from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

API_TOKEN = "714bf56178b24ab6aef210524250511"
API_URL = "https://api.weatherapi.com/v1/forecast.json"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def weather_message(temp, condition):
    c = condition.lower()
    if "rain" in c or "ploaie" in c:
        return "Ia umbrela cu tine ☔"
    elif "snow" in c:
        return "Prea frig, pregătește sania! ❄️"
    elif temp > 30:
        return "Nu uita crema de soare! ☀️"
    elif temp > 20:
        return "O zi perfectă pentru plimbare! 🌤️"
    elif temp >= 10:
        return "Temperatură plăcută 🙂"
    else:
        return "Îmbracă-te bine! 🧥"


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = {}
    message = ""

    hourly_temps = []
    hourly_wind = []
    hourly_humidity = []
    hour_labels = []

    daily_labels = []
    daily_max = []
    daily_min = []

    if request.method == "POST":
        city = request.form.get("city")

        try:
            response = requests.get(
                API_URL,
                params={
                    "key": API_TOKEN,
                    "q": city,
                    "days": 3,  
                    "aqi": "no",
                    "alerts": "no"
                }
            )

            data = response.json()

            weather = {
                "temperature": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "uv": data["current"]["uv"],
                "wind_kph": data["current"]["wind_kph"],
                "feelslike_c": data["current"]["feelslike_c"],
                "pressure": data["current"]["pressure_mb"],
                "visibility": data["current"]["vis_km"],
                "lat": data["location"]["lat"],   
                "lon": data["location"]["lon"]
            }

            hourly_data = data["forecast"]["forecastday"][0]["hour"]
            hourly_temps = [h["temp_c"] for h in hourly_data]
            hourly_wind = [h["wind_kph"] for h in hourly_data]
            hourly_humidity = [h["humidity"] for h in hourly_data]
            hour_labels = [h["time"].split(" ")[1] for h in hourly_data]

       
            for day in data["forecast"]["forecastday"]:
                daily_labels.append(day["date"])
                daily_max.append(day["day"]["maxtemp_c"])
                daily_min.append(day["day"]["mintemp_c"])

            message = weather_message(weather["temperature"], weather["condition"])

        except Exception:
            weather = {"error": "Oraș invalid sau eroare API"}

    return render_template(
        "index.html",
        city=city,
        weather=weather,
        message=message,
        hourly_temps=hourly_temps,
        hourly_wind=hourly_wind,
        hourly_humidity=hourly_humidity,
        hour_labels=hour_labels,
        daily_labels=daily_labels,
        daily_max=daily_max,
        daily_min=daily_min
    )


@app.route("/add_favorite", methods=["POST"])
@login_required
def add_favorite():
    city = request.form.get("city")
    if city:
        favorites = current_user.favorite_cities
        if city not in favorites:
            favorites.append(city)
            current_user.favorite_cities = favorites
            db.session.commit()
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not User.query.filter_by(username=request.form["username"]).first():
            user = User(
                username=request.form["username"],
                password_hash=generate_password_hash(request.form["password"])
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/metrics")
def metric_data():
    city = "Bucharest"

    hourly_temps = []
    hourly_wind = []
    hourly_humidity = []
    hourly_uv = []
    hour_labels = []

    daily_labels = []
    daily_max = []
    daily_min = []
    daily_precip = []
    daily_wind_avg = []
    daily_cloud = []

    try:
        response = requests.get(
            API_URL,
            params={"key": API_TOKEN, "q": city, "days": 3, "aqi": "no", "alerts": "no"}
        )
        data = response.json()

        metrics = {
            "location": data["location"]["name"],
            "country": data["location"]["country"],
            "temp_c": data["current"]["temp_c"],
            "feelslike_c": data["current"]["feelslike_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "wind_dir": data["current"]["wind_dir"],
            "pressure_mb": data["current"]["pressure_mb"],
            "uv": data["current"]["uv"],
            "cloud": data["current"]["cloud"],
            "precip_mm": data["current"]["precip_mm"],
            "visibility_km": data["current"]["vis_km"]
        }

        hourly_data = data["forecast"]["forecastday"][0]["hour"]
        for h in hourly_data:
            hour_labels.append(h["time"].split(" ")[1])
            hourly_temps.append(h["temp_c"])
            hourly_wind.append(h["wind_kph"])
            hourly_humidity.append(h["humidity"])
            hourly_uv.append(h["uv"])

        for day in data["forecast"]["forecastday"]:
            daily_labels.append(day["date"])
            daily_max.append(day["day"]["maxtemp_c"])
            daily_min.append(day["day"]["mintemp_c"])
            daily_precip.append(day["day"]["totalprecip_mm"])
            daily_wind_avg.append(day["day"]["maxwind_kph"])
            daily_cloud.append(day["day"]["avgvis_km"])  

    except Exception as e:
        metrics = {"error": str(e)}

    return render_template(
        "metric_data.html",
        metrics=metrics,
        hourly_temps=hourly_temps,
        hourly_wind=hourly_wind,
        hourly_humidity=hourly_humidity,
        hourly_uv=hourly_uv,
        hour_labels=hour_labels,
        daily_labels=daily_labels,
        daily_max=daily_max,
        daily_min=daily_min,
        daily_precip=daily_precip,
        daily_wind_avg=daily_wind_avg,
        daily_cloud=daily_cloud
    )



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(" ---> users.db creat / actualizat (user database up to date)")
    app.run(debug=True)
