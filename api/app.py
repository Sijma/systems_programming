from flask import Flask, request
from flask_cors import CORS
from recommendations import get_recommendation_coupon, recommendation_registry
import schemas

app = Flask(__name__)
app.json.sort_keys = False
CORS(app, resources={r"/*": {"origins": "http://localhost"}})

@app.route('/api/', methods=["GET"])
def home():
    return "hello world!"

@app.route('/api/recommend', methods=["POST"])
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = get_recommendation_coupon(recommendation_registry, request.json["generator"], request.json["user_id"], request.json["amount"])
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")
