import os
import json
import random
from datetime import datetime
from time import sleep
from confluent_kafka import Producer

MESSAGES_PER_SECOND = 1
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
    producer.produce("user", value=json.dumps(user))


while True:
    publish_user(generate_random_user())
    sleep(__time_to_sleep)
