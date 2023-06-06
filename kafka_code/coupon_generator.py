import os
import json
import random
import uuid
from datetime import datetime, timedelta
from time import sleep
from confluent_kafka import Producer

from database import Database

MESSAGES_PER_SECOND = 10
__time_to_sleep = 1 / MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})
db = Database()

def generate_selections(coupon_timestamp):
    event_id = db.get_random_event_id_after_timestamp(coupon_timestamp)
    if event_id is None:
        return None
    outcome = random.choice(['home win', 'away win', 'draw'])
    odds = random.uniform(1.0, 2.0)

    selection = {"event_id": event_id, "outcome": outcome, "odds": odds}

    return selection

def generate_random_coupon():
    coupon_timestamp = datetime.now() - timedelta(days=random.randint(0, 90))
    user_id = db.get_random_user_id()

    num_selections = random.randint(1, 10)
    selections = []

    while len(selections) < num_selections:
        selection = generate_selections(coupon_timestamp)
        if selection is not None:
            selections.append(selection)

    coupon = {
        "coupon_id": str(uuid.uuid4()),
        "selections": selections,
        "stake": random.uniform(1.0, 10.0),
        "timestamp": coupon_timestamp.isoformat(),
        "user_id": user_id
    }
    return coupon


def publish_coupon(coupon):
    producer.produce("coupon", value=json.dumps(coupon))


if __name__ == '__main__':
    while True:
        publish_coupon(generate_random_coupon())
        sleep(__time_to_sleep)
