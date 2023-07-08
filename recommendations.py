import random
import requests

def dummy_generator(user_id, recommendation_amount):
    return {
        "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
        "selections": [
            {
                "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                "outcome": "away win",
                "odds": 3.97
            },
            {
                "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                "outcome": "away win",
                "odds": 2.9
            },
            {
                "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                "outcome": "away win",
                "odds": 4.91
            }
        ],
        "stake": 40.8,
        "timestamp": "2020-01-01101:05:01",
        "user_id": user_id
    }


def random_generator(user_id, recommendation_amount):
    recommendations_list = [{
        "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
        "selections": [
            {
                "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                "outcome": "away win",
                "odds": 3.97
            },
            {
                "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                "outcome": "away win",
                "odds": 2.9
            },
            {
                "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                "outcome": "away win",
                "odds": 4.91
            }
        ],
        "stake": 40.8,
        "timestamp": "2020-01-01101:05:01",
        "user_id": user_id
    }, {
        "coupon_id": "b3a3e24c-fb9e-4ed1-9bb4-321cb7a2bc1f",
        "selections": [
            {
                "event_id": "a5a7a5d5-c5f7-4b33-8dcb-04f757e9a7a9",
                "outcome": "away win",
                "odds": 2.15
            },
            {
                "event_id": "d8f6c1b6-95de-438c-b6d8-72e79b78aa0b",
                "outcome": "away win",
                "odds": 1.85
            },
            {
                "event_id": "8d3c3e1e-2b54-4c3a-97e4-93b70ca23b7f",
                "outcome": "away win",
                "odds": 4.28
            },
            {
                "event_id": "fc8dc476-9c70-4217-bb2d-74d820a6c740",
                "outcome": "away win",
                "odds": 2.6
            }
        ],
        "stake": 25.0,
        "timestamp": "2022-02-22T08:15:30Z",
        "user_id": user_id
    }, {
        "coupon_id": "87a74a51-8d4d-4ecf-a5b5-623042c8bb6b",
        "selections": [
            {
                "event_id": "d89aa157-efc6-481a-a2aa-1c615d9a9f62",
                "outcome": "away win",
                "odds": 1.67
            }
        ],
        "stake": 15.0,
        "timestamp": "2023-04-30T12:00:00Z",
        "user_id": user_id

    }]

    random_int = random.randint(0, 2)  # inclusive

    return recommendations_list[random_int]

def get_most_played_events(amount):
    url = f"http://localhost:8000/most_played_events/{amount}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data['events']

def popular_generator(user_id, recommendation_amount):
    events = get_most_played_events(recommendation_amount)
    selections = []
    for event in events:
        event_id, outcome, coupon_count = event
        selections.append({"event_id": event_id, "outcome": outcome, "coupon_count": coupon_count})
    return {"selections": selections}

recommendation_registry = {
    "dummy": dummy_generator,
    "random": random_generator,
    "popular": popular_generator
}


def get_recommendation_coupon(registry, generator_type, user_id, recommendation_amount):
    return registry[generator_type](user_id, recommendation_amount)
