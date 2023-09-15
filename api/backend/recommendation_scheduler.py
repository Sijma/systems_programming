import datetime
from .models import Subscriber
from flask_mail import Message
from . import mail, MAIL_USERNAME
from .recommendations import get_recommendation_coupon
import json
from sqlalchemy import or_


def get_subscriptions():
    today = datetime.date.today()
    is_monday = today.weekday() == 0  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    is_first_day_of_month = today.day == 1  # True if 1st of month

    conditions = [Subscriber.frequency == 'daily']
    if is_monday:
        conditions.append(Subscriber.frequency == 'weekly')
    if is_first_day_of_month:
        conditions.append(Subscriber.frequency == 'monthly')

    combined_condition = or_(*conditions)
    subscriptions = Subscriber.query.filter(combined_condition).all()

    return subscriptions


def send_recommendations(subscriptions):
    cache = {}
    for subscription in subscriptions:
        user_id = subscription.id
        email = subscription.email
        recommender = subscription.recommender
        num_recommendations = subscription.num_recommendations

        cached_recommendations = cache.get(recommender)

        if cached_recommendations is None:
            res = get_recommendation_coupon(recommender, user_id, 10)  # TODO: Change to rec_amount MAX
            selections = res.get("selections")
            cached_recommendations = cache[recommender] = selections

        to_email = json.dumps({"selections": cached_recommendations[:num_recommendations]})

        msg = Message('Recommendation Subscription', sender=MAIL_USERNAME, recipients=[email])
        msg.body = to_email
        mail.send(msg)


if __name__ == "__main__":
    subs = get_subscriptions()
    send_recommendations(subs)
