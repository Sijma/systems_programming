import unittest
from unittest.mock import MagicMock, patch
import app
from app import app as app_client
from jsonschema import ValidationError
import recommendations
import schemas


class TestRecommendations(unittest.TestCase):
    def test_registry_contains_expected_entries(self):
        self.assertIn("dummy", recommendations.recommendation_registry)
        self.assertIn("random", recommendations.recommendation_registry)

    def test_registry_return_values(self):
        self.assertEqual(recommendations.dummy_generator, recommendations.recommendation_registry["dummy"])
        self.assertEqual(recommendations.random_generator, recommendations.recommendation_registry["random"])

    def test_dummy(self):
        recommendation = recommendations.dummy_generator(1)
        self.assertEqual(recommendation, {
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": [
                {
                    "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                    "odds": 3.97
                },
                {
                    "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                    "odds": 2.9
                },
                {
                    "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                    "odds": 4.91
                }
            ],
            "stake": 40.8,
            "timestamp": "2020-01-01101:05:01",
            "user_id": 1
        })
        self.assertIsNone(schemas.validate(recommendation, schemas.coupon_schema))  # Is it correct to check schema here?

    @patch('recommendations.random.randint', MagicMock(return_value=0))
    def test_random0(self):
        recommendation = recommendations.random_generator(1)
        self.assertEqual(recommendation, {
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": [
                {
                    "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                    "odds": 3.97
                },
                {
                    "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                    "odds": 2.9
                },
                {
                    "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                    "odds": 4.91
                }
            ],
            "stake": 40.8,
            "timestamp": "2020-01-01101:05:01",
            "user_id": 1
        })
        self.assertIsNone(schemas.validate(recommendation, schemas.coupon_schema))
        recommendations.random.randint.assert_called_once_with(0, 2)

    @patch('recommendations.random.randint', MagicMock(return_value=1))
    def test_random1(self):
        recommendation = recommendations.random_generator(1)
        self.assertEqual(recommendation, {
            "coupon_id": "b3a3e24c-fb9e-4ed1-9bb4-321cb7a2bc1f",
            "selections": [
                {
                    "event_id": "a5a7a5d5-c5f7-4b33-8dcb-04f757e9a7a9",
                    "odds": 2.15
                },
                {
                    "event_id": "d8f6c1b6-95de-438c-b6d8-72e79b78aa0b",
                    "odds": 1.85
                },
                {
                    "event_id": "8d3c3e1e-2b54-4c3a-97e4-93b70ca23b7f",
                    "odds": 4.28
                },
                {
                    "event_id": "fc8dc476-9c70-4217-bb2d-74d820a6c740",
                    "odds": 2.6
                }
            ],
            "stake": 25.0,
            "timestamp": "2022-02-22T08:15:30Z",
            "user_id": 1
        })
        self.assertIsNone(schemas.validate(recommendation, schemas.coupon_schema))
        recommendations.random.randint.assert_called_once_with(0, 2)

    @patch('recommendations.random.randint', MagicMock(return_value=2))
    def test_random2(self):
        recommendation = recommendations.random_generator(5)
        self.assertEqual(recommendation, {
            "coupon_id": "87a74a51-8d4d-4ecf-a5b5-623042c8bb6b",
            "selections": [
                {
                    "event_id": "d89aa157-efc6-481a-a2aa-1c615d9a9f62",
                    "odds": 1.67
                }
            ],
            "stake": 15.0,
            "timestamp": "2023-04-30T12:00:00Z",
            "user_id": 5

        })
        self.assertIsNone(schemas.validate(recommendation, schemas.coupon_schema))
        recommendations.random.randint.assert_called_once_with(0, 2)

    @patch('recommendations.dummy_generator', MagicMock(return_value={
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": [
                {
                    "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                    "odds": 3.97
                },
                {
                    "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                    "odds": 2.9
                },
                {
                    "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                    "odds": 4.91
                }
            ],
            "stake": 40.8,
            "timestamp": "2020-01-01101:05:01",
            "user_id": 1
        }))
    @patch('recommendations.random_generator', MagicMock(return_value={
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": [
                {
                    "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                    "odds": 3.97
                },
                {
                    "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                    "odds": 2.9
                },
                {
                    "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                    "odds": 4.91
                }
            ],
            "stake": 40.8,
            "timestamp": "2020-01-01101:05:01",
            "user_id": 1
        }))
    def test_get_recommendation(self):
        user_id = 1

        mocked_dummy_result = recommendations.dummy_generator.return_value
        mocked_random_result = recommendations.random_generator.return_value

        mocked_registry = {
            "dummy": recommendations.dummy_generator,
            "random": recommendations.random_generator,
        }

        # Test with "dummy" generator_type
        self.assertEqual(recommendations.get_recommendation_coupon(mocked_registry, "dummy", user_id), mocked_dummy_result)
        recommendations.dummy_generator.assert_called_once_with(1)

        # Test with "random" generator_type
        self.assertEqual(recommendations.get_recommendation_coupon(mocked_registry, "random", user_id), mocked_random_result)
        recommendations.random_generator.assert_called_once_with(1)


class TestSchemas(unittest.TestCase):
    #  I assume when testing schemas we should write a test case for each possible field in the schema. But that would take a while.
    def test_valid_recommendation_request_schema(self):
        data = {"user_id": 1, "generator": "random"}
        self.assertIsNone(schemas.validate(data, schemas.recommendation_request_schema))

    def test_invalid_recommendation_request_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_request_schema)
        data = {"user_id": "a", "generator": "random"}
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_request_schema)
        data = {"user_id": 1, "generator": "rand"}
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.recommendation_request_schema)

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
            "country": "USA",  # Invalid country format
            "end_timestamp": "2023-04-29T16:00:00Z",
            "event_id": "72d8a5a5-2933-42f3-8e56-8d8dc8805c5a",
            "league": "NBA",
            "participants": ["Team A"],  # Invalid participants amount
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
        self.client = app_client.test_client()

    @patch('app.get_recommendation_coupon', MagicMock(return_value={
            "coupon_id": "87a74a51-8d4d-4ecf-a5b5-623042c8bb6b",
            "selections": [
                {
                    "event_id": "d89aa157-efc6-481a-a2aa-1c615d9a9f62",
                    "odds": 1.67
                }
            ],
            "stake": 15.0,
            "timestamp": "2023-04-30T12:00:00Z",
            "user_id": 5

        }))
    def test_get_recommendation_1(self):
        payload = {"user_id": 1, "generator": "random"}
        response = self.client.post('/recommend', json=payload)

        mocked_registry = {
            "dummy": recommendations.dummy_generator,
            "random": recommendations.random_generator,
        }

        recommendation = app.get_recommendation_coupon.return_value

        app.get_recommendation_coupon.assert_called_once_with(mocked_registry, "random", 1)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json, recommendation)

    @patch('app.get_recommendation_coupon', MagicMock(return_value={
            "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
            "selections": [
                {
                    "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
                    "odds": 3.97
                },
                {
                    "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
                    "odds": 2.9
                },
                {
                    "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
                    "odds": 4.91
                }
            ],
            "stake": 40.8,
            "timestamp": "2020-01-01101:05:01",
            "user_id": 1
        }))
    def test_get_recommendation_2(self):
        payload = {"user_id": 2, "generator": "dummy"}
        response = self.client.post('/recommend', json=payload)

        mocked_registry = {
            "dummy": recommendations.dummy_generator,
            "random": recommendations.random_generator,
        }

        recommendation = app.get_recommendation_coupon.return_value

        app.get_recommendation_coupon.assert_called_once_with(mocked_registry, "dummy", 2)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json, recommendation)


if __name__ == '__main__':
    unittest.main()
