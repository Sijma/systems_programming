import os
import json
import random
import uuid
from datetime import datetime, timedelta
from time import sleep
from confluent_kafka import Producer

MESSAGES_PER_SECOND = 10
__time_to_sleep = 1 / MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})

def generate_start_and_end_time():
    begin_timestamp = datetime.now() + timedelta(days=random.randint(-30, 30))
    end_timestamp = begin_timestamp + timedelta(hours=2)

    return begin_timestamp, end_timestamp

def generate_random_event():
    start_time, end_time = generate_start_and_end_time()
    event = {
        "begin_timestamp": start_time.isoformat(),
        "country": "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)),
        "end_timestamp": end_time.isoformat(),
        "event_id": str(uuid.uuid4()),
        "league": "Sample League",
        "home_team": random.choice(["Team A", "Team B", "Team C", "Team D", "Team E"]),
        "away_team": random.choice(["Team F", "Team G", "Team H", "Team I", "Team J"]),
    }
    return event

def publish_event(event):
    producer.produce("event", value=json.dumps(event))

if __name__ == '__main__':
    while True:
        publish_event(generate_random_event())
        sleep(__time_to_sleep)
