from flask import Blueprint, request, jsonify
from models import db, User

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users", methods=["POST"])
def create_user():

    data = request.json

    if not data.get("name") or not data.get("email") or not data.get("role"):
        return jsonify({"error": "Missing fields"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role=data["role"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201



@user_routes.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    result = []

    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        })

    return jsonify(result)
