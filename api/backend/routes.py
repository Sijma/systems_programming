from flask import Blueprint, request
from .recommendations import get_recommendation_coupon, get_available_recommenders
from flask_jwt_extended import jwt_required
import schemas

routes = Blueprint('routes', __name__)


@routes.route('/', methods=["GET"])
@jwt_required()
def home():
    return "hello world!"


@routes.route('/list-recommenders', methods=["GET"])
@jwt_required()
def get_recommenders():
    return get_available_recommenders()


@routes.route('/recommend', methods=["POST"])
@jwt_required()
@schemas.json_validator(schemas.recommendation_request_schema)
def get_recommendation():
    response = get_recommendation_coupon(request.json["generator"], request.json["user_id"], request.json["amount"])
    return response
