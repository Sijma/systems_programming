import unittest
from app import app
import json
import recommendations


class TestRecommendations(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(recommendations.dummy(1), {"recommendation": "dummy"})
        self.assertEqual(recommendations.dummy(-1), {"recommendation": "dummy"})
        self.assertEqual(recommendations.dummy(0), {"recommendation": "dummy"})
        self.assertEqual(recommendations.dummy(2), {"recommendation": "dummy"})

    def test_random(self):
        self.assertEqual(recommendations.random(1), {"recommendation": "random"})
        self.assertEqual(recommendations.random(-1), {"recommendation": "random"})
        self.assertEqual(recommendations.random(0), {"recommendation": "random"})
        self.assertEqual(recommendations.random(2), {"recommendation": "random"})


class TestApp(unittest.TestCase):
    def test_get_recommendation_odd(self):
        with app.test_client() as client:
            payload = json.dumps({"user-id": 1})
            response = client.get('/recommend', data=payload)
            data = json.loads(response.get_data(as_text=True))
            print(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, {"recommendation": "random"})

    def test_get_recommendation_even(self):
        with app.test_client() as client:
            payload = json.dumps({"user-id": 2})
            response = client.get('/recommend', data=payload)
            data = json.loads(response.get_data(as_text=True))
            print(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, {"recommendation": "dummy"})


if __name__ == '__main__':
    unittest.main()
