from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    favorite_city = db.Column(db.String(100), default="Bucharest")

    other_cities = db.Column(db.String(500), default="") 
    fav_destinations = db.Column(db.String(500), default="")
    interests = db.Column(db.String(500), default="")