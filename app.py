from flask import Flask, request
from jsonschema import validate, ValidationError
import recommendations
import schemas

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/recommend', methods=["GET"])
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = recommendations.get_recommendation_based_on_user_id(recommendations.recommendation_registry, request.json["user-id"])
    validate(response, schemas.recommendation_response_schema)
    return response


if __name__ == '__main__':
    app.run()
