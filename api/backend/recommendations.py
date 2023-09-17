import requests
from .recommendation_factory import Recommender
import os


class DummyGenerator(Recommender, cl_name="dummy"):
    @classmethod
    def recommend(cls, user_id, recommendation_amount):
        return {
            "selections": [
                {
                    "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                    "outcome": "away win",
                },
                {
                    "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                    "outcome": "away win",
                },
                {
                    "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                    "outcome": "away win",
                }
            ],
        }


class PopularGenerator(Recommender, cl_name="popular"):
    @classmethod
    def recommend(cls, user_id, recommendation_amount):
        response = requests.get(f"http://{os.environ.get('FASTAPI_HOST')}:{os.environ.get('FASTAPI_PORT')}/most_played_events/{recommendation_amount}")
        if response.status_code != 200:
            print(response.text)
            events = None
        else:
            events = response.json()['events']
        selections = []
        for event in events:
            event_id, outcome, coupon_count = event
            selections.append({"event_id": event_id, "outcome": outcome, "coupon_count": coupon_count})
        return {"selections": selections}


def get_available_recommenders():
    return list(Recommender.get_recommender_registry().keys())


def get_recommendation_coupon(generator_type, user_id, recommendation_amount):
    return Recommender.get_recommender(generator_type).recommend(user_id, recommendation_amount)
