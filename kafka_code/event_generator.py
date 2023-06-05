import os
import json
import random
import uuid
from datetime import datetime
from time import sleep
from confluent_kafka import Producer

MESSAGES_PER_SECOND = 5
__time_to_sleep = 1 / MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})

def generate_random_event():
    event = {
        "begin_timestamp": datetime.now().isoformat(),
        "country": "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)),
        "end_timestamp": datetime.now().isoformat(),
        "event_id": str(uuid.uuid4()),
        "league": "Sample League",
        "participants": [random.choice(["Team A", "Team B"]), random.choice(["Team C", "Team D"])],
        "sport": "Sample Sport"
    }
    return event

def publish_event(event):
    producer.produce("event", value=json.dumps(event))

while True:
    publish_event(generate_random_event())
    sleep(__time_to_sleep)
