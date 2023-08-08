# pyright: reportMissingImports=false, reportMissingModuleSource=false

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import redis


import datetime
import re


app = Flask(__name__)

ACCESS_EXPIRES = datetime.timedelta(minutes=30)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movieDB.sqlite"
app.config["SECRET_KEY"] = "moviecops"
app.config["JWT_SECRET_KEY"] = "moviecops"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES


jwt = JWTManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app, origins=["http://localhost:8080"])


rhost = "localhost"
rport = 6379
rdb = 0
redis_client = redis.StrictRedis(
    host=rhost, port=rport, db=rdb, decode_responses=True)


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

    def to_dict(self):
        return {
            'venue_id': self.venue_id,
            'name': self.name,
            'location': self.location
        }

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

    def to_dict(self):
        return {
            'show_id': self.show_id,
            'name': self.name,
            'rating': self.rating,
            'tags': self.tags,
            'language': self.language,
            'imagePath': self.image_src,
            'venue_id': self.venue_id,
            'price': self.ticket_price,
            'seats': self.seats,
            'timings': self.timings
        }

    def __repr__(self):
        return f"Shows(show_id={self.show_id}, name='{self.name}', rating={self.rating}, tags='{self.tags}', " \
               f"language='{self.language}', image_src='{self.image_src}', venue_id={self.venue_id}, " \
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

    def to_dict(self):
        return {
            'booking_id': self.booking_id,
            'user_email': self.user_email,
            'show_id': self.show_id,
            'venue_id': self.venue_id,
            'seat_num': self.seat_num.split(", ")
        }

    def __repr__(self):
        return f"Booking(booking_id={self.booking_id}, user_email='{self.user_email}', " \
               f"venue_id={self.venue_id}, show_id={self.show_id}, seat_num='{self.seat_num}')"


def validateLogin(name, password, admin=False):
    if not name:
        raise Exception("Email not provided!")

    if not password:
        raise Exception("Password not provided!")

    check_user = User.query.filter_by(email=name).first()
    print(check_user)
    if not check_user:
        raise Exception("Name not registered!")

    if not bcrypt.check_password_hash(check_user.password, password):
        raise Exception("Invalid password!")

    if admin and bool(check_user.admin) == False:
        raise Exception("Do not have admin privileges!")

    return True


def check_admin(current_user):
    try:
        user_data = User.query.filter_by(email=current_user).first()
        admin = bool(user_data.admin)

        if not admin:
            raise Exception("Do not have admin privileges!")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return "MovieCops API"


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_revoked = redis_client.get(jti)
    return token_revoked is not None


@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        source = request.json.get('source', False)

        validateLogin(email, password, source)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    access_token = create_access_token(identity=email)
    if source:
        return jsonify(access_token=access_token, admin=True), 200
    return jsonify(access_token=access_token), 200


@app.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        name = request.json.get('name', None)
        language = request.json.get('language', None)

        if not email:
            raise Exception("Email not provided!")

        if not bool(re.fullmatch(r'^[\w.]+@[\w.]+[.]+[\w.]+', email)):
            raise Exception("Invalid email address!")

        if not password:
            raise Exception("Password not provided!")

        if len(password) < 8:
            raise Exception("Your password must be at least 8 characters!")

        if not name:
            raise Exception("Name not provided!")

        if not language or language == "Select your preferred language":
            raise Exception("Language not provided!")

        check_user = User.query.filter_by(email=email).first()

        if check_user:
            raise Exception("Email is already in use!")

        has_uppercase = False
        has_lowercase = False
        has_digit = False
        has_special = False
        allowed_Schars = ['!', '@', '#', '$', '%']

        for char in password:
            if char.isupper():
                has_uppercase = True
            elif char.islower():
                has_lowercase = True
            elif char.isdigit():
                has_digit = True
            elif char in allowed_Schars:
                has_special = True
        if not (has_uppercase and has_lowercase and has_digit and has_special):
            raise Exception(
                "Invalid Password! Your password must contain a capital letter/ number/ special character.")

        password = bcrypt.generate_password_hash(password)

        if request.json.get('adminkey', None) == "adminKey":
            new_user = User(email=email, name=name,
                            password=password, language=language, admin=True)
        else:
            new_user = User(email=email, name=name,
                            password=password, language=language)

        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "registered user!"}), 200


@app.route('/bookticket', methods=['POST'])
@jwt_required()
def bookticket():
    try:
        current_user = get_jwt_identity()
        user_data = User.query.filter_by(email=current_user).first()

        venue_id = request.json.get('venue_id', None)
        show_id = request.json.get('show_id', None)
        seats = request.json.get('seats', None)

        if not venue_id:
            raise Exception("Venue id not provided!")

        if not show_id:
            raise Exception("Show id not provided!")

        if not seats:
            raise Exception("Seat number not provided!")

        if not user_data:
            raise Exception("User not found!")

        if len(seats) < 1:
            raise Exception("Invalid seats")

        bookings = Booking.query.filter_by(
            venue_id=venue_id, show_id=show_id).all()

        for seat in seats:
            for booking in bookings:
                if seat in booking.seat_num.split(", "):
                    raise Exception("Seat already booked!")

        new_booking = Booking(user_email=current_user,
                              venue_id=venue_id, show_id=show_id, seat_num=", ".join(seats))

        db.session.add(new_booking)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ticket booked!"}), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user_data = User.query.filter_by(email=current_user).first()

    return jsonify(logged_in_as=current_user, admin=bool(user_data.admin)), 200


@app.route('/booking/get', methods=['GET'])
@jwt_required()
def user_tickets():
    try:
        current_user = get_jwt_identity()
        user_data = User.query.filter_by(email=current_user).first()

        if not user_data:
            raise Exception("User not found!")

        bookings = db.session.query(Booking, Shows, Venue).filter(
            Booking.user_email == current_user).filter(Booking.show_id == Shows.show_id).filter(Booking.venue_id == Venue.venue_id).all()

        bookings_data = []

        for booking, show, venue in bookings:
            user_ticket = dict()
            user_ticket["name"] = show.name
            user_ticket["venue_name"] = venue.name
            user_ticket["venue_location"] = venue.location
            user_ticket["seats"] = booking.seat_num
            user_ticket["timings"] = show.timings
            user_ticket["image_src"] = show.image_src
            bookings_data.append(user_ticket)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(bookings=bookings_data), 200


@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_client.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg='Successfully logged out'), 200


@app.route('/show/get/<show_id>', methods=['GET'])
def get_bshow(show_id=None):
    try:
        if not show_id:
            raise Exception("Show id not provided!")

        query = db.session.query(Shows, Venue).filter(
            Shows.venue_id == Venue.venue_id).filter(Shows.show_id == show_id).first()

        if not query:
            raise Exception("Show not found!")

        show_data = query[0].to_dict()
        venue_data = query[1].to_dict()

        bookings = Booking.query.filter_by(
            venue_id=show_data["venue_id"], show_id=show_data["show_id"]).all()

        booked_seats = []
        for booking in bookings:
            booked_seats += booking.seat_num.split(", ")

        show_data.update({"venue_name": venue_data["name"]})
        show_data.update({"venue_location": venue_data["location"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(shows=show_data, booked_seats=booked_seats), 200


@app.route('/filter', methods=['POST'])
def filter():
    try:
        min_rating = request.json.get('minRating', 0)
        language = request.json.get('language', None)
        location = request.json.get('location', None)

        if not language:
            raise Exception("Language not provided!")

        if not location:
            raise Exception("Locaton not provided!")

        if not min_rating:
            raise Exception("Rating not provided!")

        if int(min_rating) not in range(0, 11):
            raise Exception("Invalid rating!")

        query = db.session.query(Shows, Venue).filter(
            Shows.venue_id == Venue.venue_id)

        if location != "Any":
            query = query.filter(Venue.location == location)
        if language != "Any":
            query = query.filter(Shows.language == language)
        if min_rating:
            query = query.filter(Shows.rating >= min_rating)

        res = query.all()
        result_dict_list = []
        for show, venue in res:
            show_dict = show.to_dict()
            result_dict_list.append(show_dict)

        movies_list = [] if res == 0 else result_dict_list

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(shows=movies_list), 200


@app.route('/venue/get', methods=['GET'])
@jwt_required()
def get_venues():
    current_user = get_jwt_identity()
    check_admin(current_user)

    venues = Venue.query.all()
    venue_list = [venue.to_dict() for venue in venues]
    return jsonify(venues=venue_list), 200


@app.route('/venue/create', methods=['POST'])
def venue_create():
    venue_name = request.json.get('name', None)
    venue_location = request.json.get('location', None)

    try:
        if not venue_name:
            raise Exception("Venue Name not provided!")
        if not venue_location:
            raise Exception("Venue Location not provided!")

        new_venue = Venue(name=venue_name, location=venue_location)
        db.session.add(new_venue)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(msg='Venue Created!'), 200


@app.route('/venue/update', methods=['POST'])
@jwt_required()
def venue_update():

    print(request.json)
    venue_id = request.json.get('id', None)
    venue_name = request.json.get('name', None)
    venue_location = request.json.get('location', None)

    try:
        if not venue_id:
            raise Exception("Venue ID not provided!")
        if not venue_name:
            raise Exception("Venue Name not provided!")
        if not venue_location:
            raise Exception("Venue Location not provided!")

        venue = Venue.query.filter_by(venue_id=venue_id).first()
        if not venue:
            raise Exception("Venue not found!")

        venue.name = venue_name
        venue.location = venue_location
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(msg='Venue Updated!'), 200


@app.route('/venue/delete', methods=['POST'])
@jwt_required()
def venue_delete():
    venue_id = request.json.get('venue_id', None)

    try:
        if not venue_id:
            raise Exception("Venue ID not provided!")

        venue = Venue.query.filter_by(venue_id=venue_id).first()
        if not venue:
            raise Exception("Venue not found!")

        Shows.query.filter_by(venue_id=venue_id).delete()

        db.session.delete(venue)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(msg='Venue Deleted!'), 200


@app.route('/show/get', methods=['GET'])
def get_shows():
    shows = Shows.query.all()
    show_list = [show.to_dict() for show in shows]
    return jsonify(shows=show_list), 200


@app.route('/show/create', methods=['POST'])
@jwt_required()
def show_create():
    show_name = request.json.get('movieName', None)
    show_venue = request.json.get('venue_id', None)
    show_tags = request.json.get('movieTags', None)
    show_rating = request.json.get('movieRating', None)
    show_language = request.json.get('movieLanguage', None)
    show_image = request.json.get('imageFile', None)
    show_timings = request.json.get('showTimings', None)
    show_seats = request.json.get('seats', None)
    show_price = request.json.get('ticketPrice', None)

    try:
        if not show_name:
            raise Exception("Show Name not provided!")
        if not show_venue:
            raise Exception("Show Venue not provided!")
        if not show_tags:
            raise Exception("Show Tags not provided!")
        if not show_rating:
            raise Exception("Show Rating not provided!")
        if not show_language:
            raise Exception("Show Language not provided!")
        if not show_image:
            raise Exception("Show Image not provided!")
        if not show_timings:
            raise Exception("Show Timings not provided!")
        if not show_seats:
            raise Exception("Show Seats not provided!")
        if not show_price:
            raise Exception("Show Price not provided!")

        new_show = Shows(name=show_name, venue_id=show_venue, tags=show_tags, rating=show_rating,
                         language=show_language, image_src=show_image, timings=show_timings, seats=int(show_seats), ticket_price=int(show_price))
        db.session.add(new_show)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(msg='Show Created!'), 200


@app.route('/show/update', methods=['POST'])
@jwt_required()
def show_update():

    show_id = request.json.get('show_id', None)
    show_name = request.json.get('name', None)
    show_venue = request.json.get('venue_id', None)
    show_tags = request.json.get('tags', None)
    show_rating = request.json.get('rating', None)
    show_language = request.json.get('language', None)
    show_image = request.json.get('image_src', None)
    show_timings = request.json.get('timings', None)
    show_seats = request.json.get('seats', None)
    show_price = request.json.get('ticket_price', None)

    try:
        if not show_id:
            raise Exception("Show ID not provided!")
        if not show_name:
            raise Exception("Show Name not provided!")
        if not show_venue:
            raise Exception("Show Venue not provided!")
        if not show_tags:
            raise Exception("Show Tags not provided!")
        if not show_rating:
            raise Exception("Show Rating not provided!")
        if not show_language:
            raise Exception("Show Language not provided!")
        if not show_image:
            raise Exception("Show Image not provided!")
        if not show_timings:
            raise Exception("Show Timings not provided!")
        if not show_seats:
            raise Exception("Show Seats not provided!")
        if not show_price:
            raise Exception("Show Price not provided!")

        show = Shows.query.filter_by(show_id=show_id).first()
        if not show:
            raise Exception("Show not found!")

        show.name = show_name
        show.venue_id = show_venue
        show.tags = show_tags
        show.rating = show_rating
        show.language = show_language
        show.image_src = show_image
        show.timings = show_timings
        show.seats = show_seats
        show.ticket_price = show_price
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(msg='Show Updated!'), 200


@app.route('/show/delete', methods=['POST'])
@jwt_required()
def show_delete():
    show_id = request.json.get('show_id', None)

    try:
        if not show_id:
            raise Exception("Show ID not provided!")

        show = Shows.query.filter_by(show_id=show_id).first()
        if not show:
            raise Exception("Show not found!")

        db.session.delete(show)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(msg='Show Deleted!'), 200


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'message': 'Authorization header missing!'
    }), 401


if __name__ == '__main__':
    app.run(debug=True, port=5001)
