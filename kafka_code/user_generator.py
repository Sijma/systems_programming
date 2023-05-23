import os
import json
import random
from datetime import datetime
from time import perf_counter, sleep
from confluent_kafka import Producer

MESSAGES_PER_SECOND = 10
__time_to_sleep = 1/MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})

def generate_random_user():
    user = {
        "birth_year": random.randint(1900, 2023),
        "country": "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)),
        "currency": "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)),
        "gender": random.choice(["Male", "Female", "Other"]),
        "registration_date": datetime.now().isoformat(),
        "user_id": random.randint(1, 100000)
    }
    return user

def publish_user(user):
    producer.produce("users_topic", value=json.dumps(user))

while True:
    start_time = perf_counter()
    publish_user(generate_random_user())
    end_time = perf_counter()
    sleep_time = __time_to_sleep - (end_time - start_time)
    if sleep_time > 0:
        sleep(sleep_time)