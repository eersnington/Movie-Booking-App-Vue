# pyright: reportMissingImports=false, reportMissingModuleSource=false

from datetime import datetime, timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movieDB.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"User(email='{self.email}', name='{self.name}', password='{self.password}', language='{self.language}')"


class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Venue(venue_id={self.venue_id}, name='{self.name}', location='{self.location}')"


class Shows(db.Model):
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Numeric(precision=2, scale=1), nullable=False)
    tags = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    image_src = db.Column(db.String(100), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        Venue.venue_id), nullable=False)
    ticket_price = db.Column(db.Integer, default=250, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    timings = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Shows(show_id={self.show_id}, movie_id={self.movie_id}, venue_id={self.venue_id}, " \
               f"ticket_price={self.ticket_price}, seats={self.seats}, timings='{self.timings}')"


class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), db.ForeignKey(
        Shows.show_id), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey(
        Shows.show_id), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        Venue.venue_id), nullable=False)
    seat_num = db.Column(db.String(3), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Booking(booking_id={self.booking_id}, user_email='{self.user_email}', " \
               f"venue_id={self.venue_id}, show_id={self.show_id}, seat_num='{self.seat_num}', booking_time='{self.booking_time}')"


with app.app_context():
    db.create_all()
