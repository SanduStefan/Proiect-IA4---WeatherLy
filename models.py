from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    favorite_cities_json = db.Column(db.Text, default="[]")

    @property
    def favorite_cities(self):
        return json.loads(self.favorite_cities_json)

    @favorite_cities.setter
    def favorite_cities(self, cities):
        self.favorite_cities_json = json.dumps(cities)
