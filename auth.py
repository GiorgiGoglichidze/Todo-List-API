from flask import Blueprint,Flask, request, session,jsonify
from models import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import db
from werkzeug.exceptions import BadRequest

auth = Blueprint("auth",__name__)
bcrypt = Bcrypt()


@auth.route("/login",methods = ["GET","POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password"}), 401
    
    token = create_access_token(identity=user.id)
    return jsonify({"token": token})

@auth.route("/register",methods = ["GET","POST"])
def register():
    try:
        data = request.get_json(force=True)
    except BadRequest:
        return jsonify({"message": "Invalid JSON input"}), 400

    if not data:
        return jsonify({"message": "Empty JSON body"}), 400
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400
    
    if len(email) < 4:
        return jsonify({"message": "minimum length of email should be 3 characters"}), 400
    elif len(password) < 8:
        return jsonify({"message": "minimum length of password should be 8 characters"}), 400
    elif len(name) < 2:
        return jsonify({"message": "minimum length of name shoul be 1 character"}), 400
    elif password != confirm_password:
        return jsonify({"message": "password doesn't match with confirm password "}), 400


    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.id)

    return jsonify({"token": token})