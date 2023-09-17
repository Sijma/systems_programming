from flask import Blueprint, request, jsonify
from .recommendations import get_recommendation_coupon, get_available_recommenders
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Subscriber
from . import schemas, db

routes = Blueprint('routes', __name__)


@routes.route('/', methods=["GET"])
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
    user_id = get_jwt_identity()
    response = get_recommendation_coupon(request.json["generator"], user_id, request.json["amount"])
    return response


# TODO: Validate with schema
@routes.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify(message='User not found'), 404

    existing_subscription = Subscriber.query.get(user.id)
    if existing_subscription:
        return jsonify(message='User already has a subscription'), 400

    data = request.get_json()
    subscription = Subscriber(
        id=user.id,
        email=user.email,
        recommender=data['recommender'],
        frequency=data['frequency'],
        num_recommendations=data['num_recommendations']
    )

    db.session.add(subscription)
    db.session.commit()

    return jsonify(message='Subscription added successfully'), 201


@routes.route('/view-subscription', methods=['GET'])
@jwt_required()
def view_subscription():
    user_id = get_jwt_identity()
    subscription = Subscriber.query.get(user_id)
    if not subscription:
        return jsonify(message='User does not have a subscription'), 404

    return jsonify(
        email=subscription.email,
        recommender=subscription.recommender,
        frequency=subscription.frequency,
        num_recommendations=subscription.num_recommendations,
    ), 200


# TODO: Validate with schema
@routes.route('/edit-subscription', methods=['PUT'])
@jwt_required()
def edit_subscription():
    user_id = get_jwt_identity()
    subscription = Subscriber.query.get(user_id)
    if not subscription:
        return jsonify(message='User does not have a subscription'), 404

    data = request.get_json()
    subscription.recommender = data['recommender']
    subscription.frequency = data['frequency']
    subscription.num_recommendations = data['num_recommendations']

    db.session.commit()

    return jsonify(message='Subscription updated successfully'), 200


@routes.route('/delete-subscription', methods=['DELETE'])
@jwt_required()
def delete_subscription():
    user_id = get_jwt_identity()
    subscription = Subscriber.query.get(user_id)
    if not subscription:
        return jsonify(message='User does not have a subscription'), 404

    db.session.delete(subscription)
    db.session.commit()

    return jsonify(message='Subscription deleted successfully'), 200
