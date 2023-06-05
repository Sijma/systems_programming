import os
import json
import random
import uuid
from datetime import datetime
from time import sleep
from confluent_kafka import Producer

MESSAGES_PER_SECOND = 10
__time_to_sleep = 1 / MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})


def generate_random_coupon():
    num_selections = random.randint(1, 10)
    selections = []

    for _ in range(num_selections):
        selection = {
            "event_id": str(uuid.uuid4()),
            "odds": random.uniform(1.0, 2.0)
        }
        selections.append(selection)

    coupon = {
        "coupon_id": str(uuid.uuid4()),
        "selections": selections,
        "stake": random.uniform(1.0, 10.0),
        "timestamp": datetime.now().isoformat(),
        "user_id": random.randint(1, 100000)
    }
    return coupon


def publish_coupon(coupon):
    producer.produce("coupon", value=json.dumps(coupon))


while True:
    publish_coupon(generate_random_coupon())
    sleep(__time_to_sleep)
