import os
import json
import random
import database
from time import sleep
from confluent_kafka import Producer

MESSAGES_PER_SECOND = 1
__time_to_sleep = 1 / MESSAGES_PER_SECOND

producer = Producer({"bootstrap.servers": f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"})

def generate_winning_statistics():
    goals_scored = random.randint(2, 5)
    shots_on_target = random.randint(goals_scored + 3, goals_scored + 6)
    possession_percentage = round(random.uniform(50, 60), 2)
    pass_accuracy = round(random.uniform(70, 90), 2)

    return goals_scored, shots_on_target, possession_percentage, pass_accuracy


def generate_losing_statistics():
    goals_scored = random.randint(0, 2)
    shots_on_target = random.randint(goals_scored - 1, goals_scored + 2)
    pass_accuracy = round(random.uniform(40, 60), 2)

    return goals_scored, shots_on_target, pass_accuracy


def generate_unaffected_statistics():
    fouls_committed = random.randint(5, 15)
    corners = random.randint(0, 10)
    yellow_cards = random.randint(0, 3)
    red_cards = random.randint(0, 1)
    offsides = random.randint(0, 5)

    return fouls_committed, corners, yellow_cards, red_cards, offsides


def generate_saves(opposing_shots_on_target, opposing_goals_scored):
    min_saves = opposing_shots_on_target // 2
    max_saves = opposing_shots_on_target - opposing_goals_scored
    saves = random.randint(min_saves, max_saves)

    return saves

def generate_random_historical_data():
    event_id = database.get_random_event_id_for_statistics()

    if event_id is None:
        return None

    result = random.choice(['home win', 'away win', 'draw'])

    if result == 'home win':
        goals_scored_home, shots_on_target_home, possession_percentage_home, pass_accuracy_home = generate_winning_statistics()
        goals_scored_away, shots_on_target_away, pass_accuracy_away = generate_losing_statistics()
        possession_percentage_away = 100 - possession_percentage_home
    elif result == 'away win':
        goals_scored_away, shots_on_target_away, possession_percentage_away, pass_accuracy_away = generate_winning_statistics()
        goals_scored_home, shots_on_target_home, pass_accuracy_home = generate_losing_statistics()
        possession_percentage_home = 100 - possession_percentage_away
    else:  # draw
        goals_scored_home, shots_on_target_home, pass_accuracy_home = generate_losing_statistics()
        goals_scored_away = goals_scored_home
        shots_on_target_away = shots_on_target_home
        possession_percentage_home = 50
        possession_percentage_away = 50
        pass_accuracy_away = pass_accuracy_home

    fouls_committed_home, corners_home, yellow_cards_home, red_cards_home, offsides_home = generate_unaffected_statistics()
    fouls_committed_away, corners_away, yellow_cards_away, red_cards_away, offsides_away = generate_unaffected_statistics()

    saves_home = generate_saves(shots_on_target_away, goals_scored_away)
    saves_away = generate_saves(shots_on_target_home, goals_scored_home)

    statistics = {
        "event_id": str(event_id),
        "result": result,
        "goals_scored_home": goals_scored_home,
        "goals_scored_away": goals_scored_away,
        "shots_on_target_home": shots_on_target_home,
        "shots_on_target_away": shots_on_target_away,
        "possession_percentage_home": possession_percentage_home,
        "possession_percentage_away": possession_percentage_away,
        "pass_accuracy_home": pass_accuracy_home,
        "pass_accuracy_away": pass_accuracy_away,
        "fouls_committed_home": fouls_committed_home,
        "fouls_committed_away": fouls_committed_away,
        "corners_home": corners_home,
        "corners_away": corners_away,
        "yellow_cards_home": yellow_cards_home,
        "yellow_cards_away": yellow_cards_away,
        "red_cards_home": red_cards_home,
        "red_cards_away": red_cards_away,
        "offsides_home": offsides_home,
        "offsides_away": offsides_away,
        "saves_home": saves_home,
        "saves_away": saves_away
    }

    return statistics

def publish_statistics(statistics):
    producer.produce("statistics", value=json.dumps(statistics))

while True:
    publish_statistics(generate_random_historical_data())
    sleep(__time_to_sleep)