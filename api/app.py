from flask import request, jsonify
from recommendations import get_recommendation_coupon, get_available_recommenders
from flask_init import app
from flask_cors import CORS
import schemas


# # Route for user registration
# @app.route('/api/register', methods=["POST"])
# def register():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     email = request.json.get('email')
#
#     success, message = register_user(username, password, email)
#
#     if success:
#         return jsonify({"status": "success", "message": message}), 200
#     else:
#         return jsonify({"status": "error", "message": message}), 400
#
# # Route for user login
# @app.route('/api/login', methods=["POST"])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')
#
#     success, access_token = login_user(username, password)
#
#     if success:
#         return jsonify({"status": "success", "access_token": access_token}), 200
#     else:
#         return jsonify({"status": "error", "message": access_token}), 401
#
#
# # Route for email confirmation
# @app.route('/api/confirm/<token>', methods=["GET"])
# def confirm(token):
#     if confirm_email(token):
#         return jsonify({"status": "success", "message": "Email confirmed successfully"}), 200
#     else:
#         return jsonify({"status": "error", "message": "Invalid confirmation token"}), 400

@app.route('/api/', methods=["GET"])
def home():
    # user = get_user_by_id(user_id)
    # return f"hello {user.username}!"
    return "hello world!"


@app.route('/api/list-recommenders', methods=["GET"])
def get_recommenders():
    return get_available_recommenders()


@app.route('/api/recommend', methods=["POST"])
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = get_recommendation_coupon(request.json["generator"], request.json["user_id"], request.json["amount"])
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")
