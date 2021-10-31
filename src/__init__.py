from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import jwt
from sqlalchemy import select



app = Flask(__name__)
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)

api_cors_config = {
    "origins": ["*"],
    "methods": ["OPTIONS", "GET", "POST", "PATCH", "PUT", "DELETE"],
    "allow_headers": ["Authorization", "Content-Type", "x-access-token", "responseType"],
}

cors = CORS(app, resources={"/*": api_cors_config}, support_credentials=True)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route('/')
def hello():
  password = 'password_test'
  pass_from_db_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
  db.session.add(User(email="t10.afonso@sidi.org.br",password=pass_from_db_hash))
  db.session.commit()
  user = User.query.filter_by(email='t10.afonso@sidi.org.br').first()
  return jsonify(user.email)

@app.route('/login',  methods=['POST'])
def login():
    data = request.json if request.json is not None else request.form
    email = data['email']
    
    user = User.query.filter_by(email=email).first()
    
    try:
        JWT_PASS = "Sidi@2021"
        if user:
            password = data['password']
            use_pass = user.password
            
            print('checking pass')
            if check_password_hash(password=password, pwhash=use_pass):
                token = jwt.encode({
                    'email': user.email,
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }, JWT_PASS)
                response = {
                    "message": "token generated",
                    "token": token.decode("utf-8"),
                    "success": True,
                    "error": 0,
                    "password": user.password
                }
                return jsonify(response)
              
            else:
                raise AssertionError("Users: Password does not match the user entered!", 400)
        else:
            raise AssertionError("Users: This user does not exist or is invalid!", 400)
    except Exception as e:
        return e, 400
