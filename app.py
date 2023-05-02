from flask import Flask, request
from jsonschema import validate
from recommendations import get_recommendation_coupon, recommendation_registry
import schemas
from database import database

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/recommend', methods=["POST"])
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = get_recommendation_coupon(recommendation_registry, request.json["generator"], request.json["user_id"])
    validate(response, schemas.coupon_schema)
    return response


if __name__ == '__main__':
    app.run()
    database.test()
