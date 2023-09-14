from backend import create_app

app = create_app()

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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # TODO: Remove debug for production
