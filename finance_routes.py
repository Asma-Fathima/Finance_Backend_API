from flask import Blueprint, request, jsonify
from models import db, Record, User

finance_routes = Blueprint("finance_routes", __name__)


@finance_routes.route("/records", methods=["POST"])
def create_record():

    data = request.json

    required_fields = ["title", "amount", "type", "user_id"]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400


    user = User.query.get(data["user_id"])

    if not user:
        return jsonify({"error": "Invalid user"}), 404


    if user.role not in ["admin", "analyst"]:
        return jsonify({"error": "Permission denied"}), 403


    record = Record(
        title=data["title"],
        amount=data["amount"],
        type=data["type"],
        category=data.get("category"),
        created_by=data["user_id"]
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Record created"}), 201


@finance_routes.route("/records", methods=["GET"])
def get_records():

    records = Record.query.all()

    result = []

    for r in records:
        result.append({
            "id": r.id,
            "title": r.title,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "created_by": r.created_by
        })

    return jsonify(result)


@finance_routes.route("/records/<int:id>", methods=["PUT"])
def update_record(id):

    data = request.json

    record = Record.query.get(id)

    if not record:
        return jsonify({"error": "Record not found"}), 404


    user = User.query.get(data.get("user_id"))

    if not user:
        return jsonify({"error": "Invalid user"}), 404


    if user.role not in ["admin", "analyst"]:
        return jsonify({"error": "Permission denied"}), 403


    record.title = data.get("title", record.title)
    record.amount = data.get("amount", record.amount)
    record.type = data.get("type", record.type)
    record.category = data.get("category", record.category)

    db.session.commit()

    return jsonify({"message": "Record updated"})



@finance_routes.route("/records/<int:id>", methods=["DELETE"])
def delete_record(id):

    data = request.json

    record = Record.query.get(id)

    if not record:
        return jsonify({"error": "Record not found"}), 404


    user = User.query.get(data.get("user_id"))

    if not user or user.role != "admin":
        return jsonify({"error": "Only admin can delete"}), 403


    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Record deleted"})



@finance_routes.route("/summary", methods=["GET"])
def summary():

    income = db.session.query(
        db.func.sum(Record.amount)
    ).filter(Record.type == "income").scalar() or 0


    expense = db.session.query(
        db.func.sum(Record.amount)
    ).filter(Record.type == "expense").scalar() or 0


    return jsonify({
        "total_income": income,
        "total_expense": expense
    })
