from flask import Flask, request
from jsonschema import validate, ValidationError
import json
import recommendations
import schemas

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/recommend', methods=["GET"])
def get_recommendation():
    request_json = json.loads(request.data)
    try:
        validate(request_json, schemas.recommendation_request_schema)
    except ValidationError as e:
        return {'error': 'Invalid request', 'details': str(e)}, 400

    response = recommendations.get_recommendation_based_on_user_id(recommendations.recommendation_registry, request_json["user-id"])
    validate(response, schemas.recommendation_response_schema)
    return response


if __name__ == '__main__':
    app.run()
