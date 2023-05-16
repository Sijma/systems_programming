from flask import Flask, request
from models import User, Coupon, Event, Selection, db
import schemas
from recommendations import get_recommendation_coupon, recommendation_registry

from urllib import parse


app = Flask(__name__)
app.json.sort_keys = False
password = parse.quote_plus("Xq8@SHF0S1&sM7v3")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://coupon_recommendation_system:{password}@localhost/betting_recommendation_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/recommend', methods=["POST"])
@schemas.json_validator(schemas.recommendation_request_schema, schemas.coupon_schema)
def get_recommendation():
    response = get_recommendation_coupon(recommendation_registry, request.json["generator"], request.json["user_id"])
    return response


@app.route('/register', methods=["POST"])
def register():
    user = User(request.get_json())
    db.session.add(user)
    db.session.commit()
    return str(user.user_id)


if __name__ == '__main__':
    app.run()
