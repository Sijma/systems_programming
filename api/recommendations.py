# import requests
from recommendation_factory import Recommender


class DummyGenerator(Recommender, cl_name="dummy"):
    @classmethod
    def recommend(cls, user_id, recommendation_amount):
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


class PopularGenerator(Recommender, cl_name="popular"):
    @classmethod
    def recommend(cls, user_id, recommendation_amount):
        url = f"http://localhost:8000/most_played_events/{recommendation_amount}"
        response = requests.get(url)
        if response.status_code != 200:
            events =  None
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
