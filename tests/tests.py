import unittest
from unittest import mock
from app import app
from jsonschema import ValidationError, validate
import json
import recommendations
import schemas


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


class TestSchemas(unittest.TestCase):
    #  I assume when testing schemas we should write a test case for each possible field in the schema. But that would take a while.
    def test_valid_recommendation_request_schema(self):
        data = {"user-id": 1}
        self.assertIsNone(schemas.validate(data, schemas.recommendation_request_schema))

    def test_invalid_recommendation_request_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_request_schema)
        data = {"user-id": "a"}
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_request_schema)

    def test_valid_recommendation_response_schema(self):
        data = {"recommendation": "Buy stock XYZ"}
        self.assertIsNone(schemas.validate(data, schemas.recommendation_response_schema))

    def test_invalid_recommendation_response_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_response_schema)
        data = {56}
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_response_schema)

    def test_valid_user_schema(self):
        data = {
            "birth_year": 2000,
            "country": "USA",
            "currency": "USD",
            "gender": "Male",
            "registration_date": "2022-01-01T00:00:00Z",
            "user_id": 1
        }
        self.assertIsNone(schemas.validate(data, schemas.user_schema))

    def test_invalid_user_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.user_schema)
        data = {
            "birth_year": 1899,  # Invalid birth year
            "country": "USA",
            "currency": "USD",
            "gender": "Male",
            "registration_date": "2022-01-01T00:00:00Z",
            "user_id": 1
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.user_schema)
        data = {
            "birth_year": 2000,
            "country": "USA",
            "currency": "usd",  # Invalid currency format
            "gender": "Male",
            "registration_date": "2022-01-01T00:00:00Z",
            "user_id": 1
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.user_schema)

    def test_valid_event_schema(self):
        data = {
            "begin_timestamp": "2022-01-01T00:00:00Z",
            "country": "USA",
            "end_timestamp": "2022-01-01T01:00:00Z",
            "event_id": "c09163a4-4e54-4f4a-ae26-4e18c5b5f16a",
            "league": "NFL",
            "participants": ["Team A", "Team B"],
            "sport": "Football"
        }
        self.assertIsNone(schemas.validate(data, schemas.event_schema))

    def test_invalid_event_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.event_schema)

        data = {
            "begin_timestamp": "2023-04-29T14:00:00Z",
            "country": "US",  # Invalid country format
            "end_timestamp": "2023-04-29T16:00:00Z",
            "event_id": "72d8a5a5-2933-42f3-8e56-8d8dc8805c5a",
            "league": "NBA",
            "participants": ["Team A", "Team B"],
            "sport": "Basketball"
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.event_schema)

        data = {
            "begin_timestamp": "2023-04-29T14:00:00Z",
            "country": "USA",
            "end_timestamp": "2023-04-29T16:00:00Z",
            "event_id": "invalid_uuid",  # Invalid pattern for event_id
            "league": "NBA",
            "participants": ["Team A", "Team B"],
            "sport": "Basketball"
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.event_schema)

    def test_valid_coupon_schema(self):
        data = {
            "coupon_id": "0f21a456-c13d-4ed2-8c20-72f34d05dd51",
            "selections": [
                {
                    "event_id": "6b3aa548-3c79-485d-b1c5-eb064f3725c5",
                    "odds": 1.5
                },
                {
                    "event_id": "c4d51a0e-b1b6-4d14-ae5a-bdb8d84f4964",
                    "odds": 2.2
                }
            ],
            "stake": 10.5,
            "timestamp": "2023-04-29T12:30:00Z",
            "user_id": 1
        }
        self.assertIsNone(schemas.validate(data, schemas.coupon_schema))

    def test_invalid_coupon_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.coupon_schema)

        data = {
            "coupon_id": "invalid id",  # Invalid coupon_id
            "selections": [
                {
                    "event_id": "6b3aa548-3c79-485d-b1c5-eb064f3725c5",
                    "odds": 1.5
                },
                {
                    "event_id": "c4d51a0e-b1b6-4d14-ae5a-bdb8d84f4964",
                    "odds": 2.2
                }
            ],
            "stake": 10.5,
            "timestamp": "2023-04-29T12:30:00Z",
            "user_id": 1
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.coupon_schema)

        data = {
            "coupon_id": "0f21a456-c13d-4ed2-8c20-72f34d05dd51",
            "selections": [
                {
                    "event_id": "6b3aa548-3c79-485d-b1c5-eb064f3725c5",
                    "odds": 1.5
                },
                {
                    "event_id": "c4d51a0e-b1b6-4d14-ae5a-bdb8d84f4964",
                    "odds": 2.2
                }
            ],
            "stake": "invalid stake",  # Invalid stake
            "timestamp": "2023-04-29T12:30:00Z",
            "user_id": 1
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.coupon_schema)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('app.get_recommendation_based_on_user_id', wraps=recommendations.get_recommendation_based_on_user_id)  # Is this correct?
    @mock.patch('app.validate', wraps=validate)  # Is this correct?
    def test_get_recommendation_odd(self, mock_validate, mock_get_recommendation_based_on_user_id):
        payload = {"user-id": 1}
        response = self.client.post('/recommend', json=payload)

        mock_get_recommendation_based_on_user_id.assert_called_once_with(recommendations.recommendation_registry, payload["user-id"])  # Is this correct?
        mock_validate.assert_called_once_with(response.json, schemas.recommendation_response_schema)  # Is this correct?

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertIsNone(schemas.validate(response.json, schemas.recommendation_response_schema))
        self.assertEqual(response.json, {"recommendation": "random"})

    @mock.patch('app.get_recommendation_based_on_user_id', return_value={"recommendation": "random"})  # Is this correct?
    @mock.patch('app.validate', return_value=None)  # Is this correct?
    def test_get_recommendation_odd_2(self, mock_validate, mock_get_recommendation_based_on_user_id):
        payload = {"user-id": 1}
        response = self.client.post('/recommend', json=payload)

        mock_get_recommendation_based_on_user_id.assert_called_once_with(recommendations.recommendation_registry, 1)  # Is this correct?
        mock_validate.assert_called_once_with({"recommendation": "random"}, schemas.recommendation_response_schema)  # Is this correct?

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertIsNone(schemas.validate(response.json, schemas.recommendation_response_schema))
        self.assertEqual(response.json, {"recommendation": "random"})

    @mock.patch('app.get_recommendation_based_on_user_id', return_value={"recommendation": "dummy"})  # Is this correct?
    @mock.patch('app.validate', return_value=None)  # Is this correct?
    def test_get_recommendation_even(self, mock_validate, mock_get_recommendation_based_on_user_id):
        payload = {"user-id": 2}
        response = self.client.post('/recommend', json=payload)

        mock_get_recommendation_based_on_user_id.assert_called_once_with(recommendations.recommendation_registry, 2)
        mock_validate.assert_called_once_with({"recommendation": "dummy"}, schemas.recommendation_response_schema)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertIsNone(schemas.validate(response.json, schemas.recommendation_response_schema))
        self.assertEqual(response.json, {"recommendation": "dummy"})


if __name__ == '__main__':
    unittest.main()
