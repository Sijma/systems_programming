from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from recommendations import get_recommendation_coupon, recommendation_registry
from flask_init import app
from user_management import get_user_by_id, register_user, confirm_email, login_user
import schemas

@app.route('/api/', methods=["GET"])
@jwt_required()
def home():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    return f"hello {user.username}!"

# Route for user registration
@app.route('/api/register', methods=["POST"])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    success, message = register_user(username, password, email)

    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 400

# Route for user login
@app.route('/api/login', methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    success, access_token = login_user(username, password)

    if success:
        return jsonify({"status": "success", "access_token": access_token}), 200
    else:
        return jsonify({"status": "error", "message": access_token}), 401

# Route for email confirmation
@app.route('/api/confirm/<token>', methods=["GET"])
def confirm(token):
    if confirm_email(token):
        return jsonify({"status": "success", "message": "Email confirmed successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid confirmation token"}), 400

@app.route('/api/recommend', methods=["POST"])
@jwt_required()
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = get_recommendation_coupon(recommendation_registry, request.json["generator"], request.json["user_id"], request.json["amount"])
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0")
