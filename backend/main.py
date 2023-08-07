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
CORS(app)


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

    def __repr__(self):
        return f"Booking(booking_id={self.booking_id}, user_email='{self.user_email}', movie_id={self.movie_id}, " \
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


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user_data = User.query.filter_by(email=current_user).first()

    return jsonify(logged_in_as=current_user, admin=bool(user_data.admin)), 200


@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_client.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg='Successfully logged out'), 200


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'message': 'Authorization header missing!'
    }), 401


if __name__ == '__main__':
    app.run(debug=True, port=5001)
