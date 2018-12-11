from groc4 import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class GrocList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    finished = db.Column(db.Boolean, default=False)


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer)
    item = db.Column(db.Text)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)






