from datetime import datetime
from server import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    transactions = db.relationship('Transaction', backref='abuzer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.balance}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    bot_id = db.Column(db.Integer,db.ForeignKey('bot.id') ,nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Transaction('{self.id}', '{self.user_id}', '{self.date}', '{self.bot_id}')"

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    info = db.Column(db.String(1000))
    bots = db.relationship('Transaction', backref='komur', lazy=True)

    def __repr__(self):
        return f"Bot('{self.id}', '{self.name}', '{self.price}')"

class Binance_Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    api_key = db.Column(db.String(100), nullable=False, default="-")
    api_secret = db.Column(db.String(100), nullable=False, default="-")

    def __repr__(self):
        return f"Bot('{self.id}', '{self.name}', '{self.price}')"
