import os
from confluent_kafka import Consumer
from database import Database
import json
from schemas import TYPE_USER, TYPE_EVENT, TYPE_COUPON, TYPE_STATISTICS
from multiprocessing import Process
import sys

conf = {
    'bootstrap.servers': f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}",
    'auto.offset.reset': 'earliest',
    'group.id': 'consumer_group',
    'enable.auto.commit': False
}

topics = [TYPE_USER, TYPE_EVENT, TYPE_COUPON, TYPE_STATISTICS]

print("connected")

buffer_size = 100

def process_messages(topic):
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    db = Database()

    buffer = []
    while True:
        msg = consumer.poll()

        if not msg.error():
            value = json.loads(msg.value().decode('utf-8'))
            if topic == TYPE_COUPON: # TODO: Look for a more elegant fix
                value["selections"] = json.dumps(value["selections"])
            buffer.append(value)

            if len(buffer) >= buffer_size:
                db.insert(buffer, topic, True)

                buffer = []
            consumer.commit(msg)

        else:
            print(f'Error occurred: {msg.error().str()}')

# Create a separate process for each topic
processes = []
for topic in topics:
    p = Process(target=process_messages, args=(topic,))
    print(p)
    p.start()
    processes.append(p)

# Here, in order to 'scale out' further than 1 process per topic, we can break down each topic into multiple partitions
# and assign them to 'balanced consumers'
# or use https://github.com/confluentinc/parallel-consumer not sure if there's one for python

# As for scaling up, we can simply allocate more resources to the docker container that is running this consumer

try:
    # `Main process` waits for KeyboardInterrupt
    while True:
        pass

except KeyboardInterrupt:
    print('KeyboardInterrupt: Stopping consumers and threads...')
    for p in processes:
        p.join()

    print('Consumers and threads stopped gracefully.')
    sys.exit(0)
