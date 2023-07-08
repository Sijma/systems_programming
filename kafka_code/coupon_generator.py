import os
import json
import random
import uuid
from datetime import datetime, timedelta
from time import sleep
from confluent_kafka import Producer
import requests


MESSAGES_PER_SECOND = 1
__time_to_sleep = 1 / MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})
base_database_url = f"http://{os.environ.get('FASTAPI_HOST')}:{os.environ.get('FASTAPI_PORT')}"

def get_random_user_id():
    url = f"{base_database_url}/random_user/"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    user_id = response.json().get("user_id")
    return user_id

def get_random_event_id_after_timestamp(coupon_timestamp):
    str_timestamp = coupon_timestamp.isoformat()
    url = f"{base_database_url}/random_event/{str_timestamp}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    event_id = response.json().get("event_id")
    return event_id


def generate_selections(coupon_timestamp):
    event_id = get_random_event_id_after_timestamp(coupon_timestamp)
    if event_id is None:
        return None
    outcome = random.choice(['home win', 'away win', 'draw'])
    odds = random.uniform(1.0, 2.0)

    selection = {"event_id": event_id, "outcome": outcome, "odds": odds}

    return selection

def generate_random_coupon():
    coupon_timestamp = datetime.now() - timedelta(days=random.randint(0, 90))
    user_id = get_random_user_id()

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
