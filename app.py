from flask import Flask, request
from recommendations import get_recommendation_coupon, recommendation_registry
import schemas
import database as db

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/', methods=["GET"])
def home():
    return "hello world!"


@app.route('/recommend', methods=["POST"])
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = get_recommendation_coupon(recommendation_registry, request.json["generator"], request.json["user_id"])
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")
