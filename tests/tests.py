import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import json
from api.app import app as app_client
from jsonschema import ValidationError
import schemas

import sys
sys.path.append('./kafka_code')
import statistics_generator, user_generator, event_generator, coupon_generator

class TestSchemas(unittest.TestCase):
    #  I assume when testing schemas we should write a test case for each possible field in the schema. But that would take a while.
    def test_valid_recommendation_request_schema(self):
        data = {"user_id": 1, "generator": "random", "amount": 3}
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
            "home_team": "Team A",
            "away_team": "Team B",
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
            "home_team": "Team A",
            # Missing away_team
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
            "home_team": "Team A",
            "away_team": "Team B",
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
                    "outcome": "away win",
                    "odds": 1.5
                },
                {
                    "event_id": "c4d51a0e-b1b6-4d14-ae5a-bdb8d84f4964",
                    "outcome": "away win",
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
                    "outcome": "away win",
                    "odds": 1.5
                },
                {
                    "event_id": "c4d51a0e-b1b6-4d14-ae5a-bdb8d84f4964",
                    "outcome": "away win",
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
                    "outcome": "away win",
                    "odds": 1.5
                },
                {
                    "event_id": "c4d51a0e-b1b6-4d14-ae5a-bdb8d84f4964",
                    "outcome": "away win",
                    "odds": 2.2
                }
            ],
            "stake": "invalid stake",  # Invalid stake
            "timestamp": "2023-04-29T12:30:00Z",
            "user_id": 1
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.coupon_schema)

    def test_valid_historical_events_schema(self):
        data = {
            "event_id": "0f21a456-c13d-4ed2-8c20-72f34d05dd51",
            "result": "home win",
            "goals_scored_home": 2,
            "goals_scored_away": 1,
            "shots_on_target_home": 5,
            "shots_on_target_away": 3,
            "total_shots_home": 10,
            "total_shots_away": 8,
            "possession_percentage_home": 58.5,
            "possession_percentage_away": 41.5,
            "pass_accuracy_home": 85.2,
            "pass_accuracy_away": 78.9,
            "fouls_committed_home": 12,
            "fouls_committed_away": 8,
            "corners_home": 4,
            "corners_away": 6,
            "yellow_cards_home": 2,
            "yellow_cards_away": 3,
            "red_cards_home": 0,
            "red_cards_away": 1,
            "offsides_home": 1,
            "offsides_away": 2,
            "saves_home": 3,
            "saves_away": 5
        }
        self.assertIsNone(schemas.validate(data, schemas.statistics_schema))

    def test_invalid_historical_events_schema(self):
        data = "invalid json"
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.statistics_schema)

        data = {
            "event_id": "invalid id",  # Invalid event_id
            "result": "home win",
            "goals_scored_home": 2,
            "goals_scored_away": 1,
            "shots_on_target_home": 5,
            "shots_on_target_away": 3,
            "total_shots_home": 10,
            "total_shots_away": 8,
            "possession_percentage_home": 58.5,
            "possession_percentage_away": 41.5,
            "pass_accuracy_home": 85.2,
            "pass_accuracy_away": 78.9,
            "fouls_committed_home": 12,
            "fouls_committed_away": 8,
            "corners_home": 4,
            "corners_away": 6,
            "yellow_cards_home": 2,
            "yellow_cards_away": 3,
            "red_cards_home": 0,
            "red_cards_away": 1,
            "offsides_home": 1,
            "offsides_away": 2,
            "saves_home": 3,
            "saves_away": 5
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.statistics_schema)

        data = {
            "event_id": "0f21a456-c13d-4ed2-8c20-72f34d05dd51",
            "result": "home win",
            "goals_scored_home": 2,
            "goals_scored_away": 1,
            "shots_on_target_home": 5,
            "shots_on_target_away": 3,
            "total_shots_home": 10,
            "total_shots_away": 8,
            "possession_percentage_home": 58.5,
            "possession_percentage_away": 41.5,
            "pass_accuracy_home": 85.2,
            "pass_accuracy_away": 78.9,
            "fouls_committed_home": 12,
            "fouls_committed_away": 8,
            "corners_home": 4,
            "corners_away": 6,
            "yellow_cards_home": 2,
            "yellow_cards_away": 3,
            "red_cards_home": 0,
            "red_cards_away": 1,
            "offsides_home": 1,
            # Missing offsides_away
            "saves_home": 3,
            "saves_away": 5
        }
        with self.assertRaises(ValidationError):
            schemas.validate(data, schemas.statistics_schema)

# class TestDatabase(unittest.TestCase):
#     def setUp(self):
#         self.db = Database()
#
#     def tearDown(self):
#         Database._instance = None # 'Reset' the singleton
#
#     def test_context_manager_usage(self):
#         self.db.connection_pool = MagicMock()
#         mock_conn = MagicMock()
#         mock_cur = MagicMock()
#         self.db.connection_pool.getconn.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#
#         with self.db:
#             self.assertEqual(self.db.cur, mock_cur)
#
#         self.db.connection_pool.getconn.assert_called_once()
#         self.db.conn.cursor.assert_called_once()
#         self.db.cur.close.assert_called_once()
#         self.db.connection_pool.putconn.assert_called_once_with(mock_conn)
#
#     def test_single_json_object(self):
#         json_data = {"user_id": 1, "birth_year": 1990, "country": "USA"}
#         data_type = 'user'
#         batch = False
#
#         query, values = construct_query(json_data, data_type, batch)
#
#         expected_query = "INSERT INTO users (user_id, birth_year, country) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
#         expected_values = (1, 1990, "USA")
#
#         self.assertEqual(query, expected_query)
#         self.assertEqual(values, expected_values)
#
#     def test_json_array(self):
#         json_data = [{"user_id": 1, "birth_year": 1990, "country": "USA"}, {"user_id": 2, "birth_year": 1985, "country": "Canada"}]
#         data_type = 'user'
#         batch = True
#
#         query, values = construct_query(json_data, data_type, batch)
#
#         expected_query = "INSERT INTO users (user_id, birth_year, country) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
#         expected_values = [(1, 1990, "USA"), (2, 1985, "Canada")]
#
#         self.assertEqual(query, expected_query)
#         self.assertEqual(values, expected_values)
#
#     def test_insert_single(self):
#         self.db.connection_pool = MagicMock()
#         mock_conn = MagicMock()
#         mock_cur = MagicMock()
#         self.db.connection_pool.getconn.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#
#         data_json = {'user_id': '1', 'birth_year': '2000', 'country': 'US', 'currency': 'USD', 'gender': 'M',
#                      'registration_date': '2021-01-01'}
#         data_type = 'user'
#
#         self.db.insert(data_json, data_type, batch=False)
#
#         self.db.connection_pool.getconn.assert_called_once()
#         mock_conn.cursor.assert_called_once()
#         mock_cur.execute.assert_called_once()
#         mock_conn.commit.assert_called_once()
#         mock_cur.close.assert_called_once()
#         self.db.connection_pool.putconn.assert_called_once_with(mock_conn)
#
#
#     def test_insert_batch(self):
#         self.db.connection_pool = MagicMock()
#         mock_conn = MagicMock()
#         mock_cur = MagicMock()
#         self.db.connection_pool.getconn.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#
#         data_json = [{'user_id': '1', 'birth_year': '2000', 'country': 'US', 'currency': 'USD', 'gender': 'M',
#                       'registration_date': '2021-01-01'}]
#         data_type = 'user'
#
#         self.db.insert(data_json, data_type, batch=True)
#
#         self.db.connection_pool.getconn.assert_called_once()
#         mock_conn.cursor.assert_called_once()
#         mock_cur.executemany.assert_called_once()
#         mock_conn.commit.assert_called_once()
#         mock_cur.close.assert_called_once()
#         self.db.connection_pool.putconn.assert_called_once_with(mock_conn)
#
#     def test_connection_and_cursor_cleanup_on_error(self):
#         self.db.connection_pool = MagicMock()
#         mock_conn = MagicMock()
#         mock_cur = MagicMock()
#         self.db.connection_pool.getconn.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#
#         data_json = {
#             'user_id': 1,
#             'birth_year': 1990,
#             'country': 'USA',
#             'currency': 'USD',
#             'gender': 'Male',
#             'registration_date': '2023-01-01'
#         }
#         data_type = schemas.TYPE_USER
#
#         mock_cur.execute.side_effect = Exception('Test error')
#
#         with self.assertRaises(Exception):
#             self.db.insert(data_json, data_type, batch=False)
#
#         self.db.connection_pool.getconn.assert_called_once()
#         mock_conn.cursor.assert_called_once()
#         mock_cur.execute.assert_called_once()
#         mock_conn.rollback.assert_called_once()
#         mock_cur.close.assert_called_once()
#         self.db.connection_pool.putconn.assert_called_once_with(mock_conn)

class UserGeneratorTests(unittest.TestCase):
    def test_generate_random_user(self):
        user = user_generator.generate_random_user()

        self.assertIsInstance(user, dict)
        self.assertIsNone(schemas.validate(user, schemas.user_schema))

    @patch('user_generator.producer')
    def test_publish_user(self, mock_producer):
        user = {
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "gender": "Male",
            "registration_date": "2023-01-01",
            "user_id": 12345
        }

        user_generator.publish_user(user)

        mock_producer.produce.assert_called_once_with("user", value=json.dumps(user))

class EventGeneratorTests(unittest.TestCase):
    def test_generate_start_and_end_time(self):
        time_now = datetime.now()

        begin_timestamp, end_timestamp = event_generator.generate_start_and_end_time()

        self.assertIsInstance(begin_timestamp, datetime)
        self.assertIsInstance(end_timestamp, datetime)
        self.assertLessEqual(begin_timestamp, end_timestamp)

        thirty_days_ago = time_now - timedelta(days=30)
        thirty_days_from_now = time_now + timedelta(days=30)
        self.assertGreaterEqual(begin_timestamp, thirty_days_ago)
        self.assertLessEqual(begin_timestamp, thirty_days_from_now)

        self.assertEqual(end_timestamp, begin_timestamp + timedelta(hours=2))

    def test_generate_random_event(self):
        event = event_generator.generate_random_event()

        self.assertIsInstance(event, dict)
        self.assertIsNone(schemas.validate(event, schemas.event_schema))

    @patch('event_generator.producer')
    def test_publish_event(self, mock_producer):
        event = {
            "begin_timestamp": "2023-01-01T19:00:00",
            "country": "USA",
            "end_timestamp": "2023-01-01T21:00:00",
            "event_id": "12345678-1234-1234-1234-1234567890AB",
            "league": "Sample League",
            "home_team": "Team A",
            "away_team": "Team B"
        }

        event_generator.publish_event(event)

        mock_producer.produce.assert_called_once_with("event", value=json.dumps(event))

class CouponGeneratorTests(unittest.TestCase):
    @patch('coupon_generator.db')
    def test_generate_selections(self, mock_db):
        coupon_timestamp = datetime.now() - timedelta(days=1)
        mock_db.get_random_event_id_after_timestamp.return_value = "c09163a4-4e54-4f4a-ae26-4e18c5b5f16a"

        selection = coupon_generator.generate_selections(coupon_timestamp)

        self.assertIsNotNone(selection)
        self.assertEqual(selection['event_id'], "c09163a4-4e54-4f4a-ae26-4e18c5b5f16a")
        self.assertIn(selection['outcome'], ['home win', 'away win', 'draw'])
        self.assertGreaterEqual(selection['odds'], 1.0)
        self.assertLessEqual(selection['odds'], 2.0)

    @patch('coupon_generator.db')
    def test_generate_random_coupon(self, mock_db):
        today = datetime.now()
        today_minus_90 = today - timedelta(days=90)

        mock_db.get_random_event_id_after_timestamp.return_value = "c09163a4-4e54-4f4a-ae26-4e18c5b5f16a"
        mock_db.get_random_user_id.return_value = 100

        coupon = coupon_generator.generate_random_coupon()

        self.assertIsNotNone(coupon)
        self.assertGreaterEqual(len(coupon['selections']), 1)
        self.assertLessEqual(len(coupon['selections']), 10)
        self.assertGreaterEqual(coupon['stake'], 1.0)
        self.assertLessEqual(coupon['stake'], 10.0)
        self.assertLessEqual(datetime.fromisoformat(coupon['timestamp']), today)
        self.assertGreaterEqual(datetime.fromisoformat(coupon['timestamp']), today_minus_90)

        self.assertIsNone(schemas.validate(coupon, schemas.coupon_schema))

    @patch('coupon_generator.producer')
    def test_publish_coupon(self, mock_producer):
        coupon = {
            "coupon_id": "12345678-1234-1234-1234-1234567890AB",
            "selections": [
                {"event_id": "event1", "outcome": "home win", "odds": 1.5},
                {"event_id": "event2", "outcome": "draw", "odds": 2.0}
            ],
            "stake": 5.0,
            "timestamp": "2023-01-01T19:00:00",
            "user_id": "user123"
        }

        coupon_generator.publish_coupon(coupon)

        mock_producer.produce.assert_called_once_with("coupon", value=json.dumps(coupon))

class StatisticsGeneratorTests(unittest.TestCase):
    def test_generate_winning_statistics(self):
        goals_scored, shots_on_target, possession_percentage, pass_accuracy = statistics_generator.generate_winning_statistics()

        self.assertGreaterEqual(goals_scored, 2)
        self.assertGreaterEqual(shots_on_target, goals_scored + 3)
        self.assertGreaterEqual(possession_percentage, 50)
        self.assertLessEqual(possession_percentage, 60)
        self.assertGreaterEqual(pass_accuracy, 70)
        self.assertLessEqual(pass_accuracy, 90)

    def test_generate_losing_statistics(self):
        goals_scored, shots_on_target, pass_accuracy = statistics_generator.generate_losing_statistics()

        self.assertGreaterEqual(goals_scored, 0)
        self.assertGreaterEqual(shots_on_target, goals_scored - 1)
        self.assertGreaterEqual(pass_accuracy, 40)
        self.assertLessEqual(pass_accuracy, 60)

    def test_generate_unaffected_statistics(self):
        fouls_committed, corners, yellow_cards, red_cards, offsides = statistics_generator.generate_unaffected_statistics()

        self.assertGreaterEqual(fouls_committed, 5)
        self.assertLessEqual(fouls_committed, 15)
        self.assertGreaterEqual(corners, 0)
        self.assertLessEqual(corners, 10)
        self.assertGreaterEqual(yellow_cards, 0)
        self.assertLessEqual(yellow_cards, 3)
        self.assertGreaterEqual(red_cards, 0)
        self.assertLessEqual(red_cards, 1)
        self.assertGreaterEqual(offsides, 0)
        self.assertLessEqual(offsides, 5)

    def test_generate_saves(self):
        opposing_shots_on_target = 10
        opposing_goals_scored = 3

        saves = statistics_generator.generate_saves(opposing_shots_on_target, opposing_goals_scored)

        self.assertGreaterEqual(saves, 0)
        self.assertLessEqual(saves, opposing_shots_on_target - opposing_goals_scored)

    @patch('statistics_generator.db')
    def test_generate_random_historical_data(self, mock_db):
        event_id = '123'
        mock_db.get_random_event_id_for_statistics.return_value = event_id

        statistics = statistics_generator.generate_random_historical_data()

        self.assertIsNotNone(statistics)
        self.assertEqual(statistics['event_id'], event_id)

        # Add more assertions to validate the generated statistics based on different result scenarios

    @patch('statistics_generator.producer')
    def test_publish_statistics(self, mock_producer):
        statistics = {
            'event_id': '6b3aa548-3c79-485d-b1c5-eb064f3725c5',
            'result': 'home win',
            'goals_scored_home': 3,
            'goals_scored_away': 1,
            'shots_on_target_home': 10,
            'shots_on_target_away': 5,
            'possession_percentage_home': 58.21,
            'possession_percentage_away': 41.79,
            'pass_accuracy_home': 84.63,
            'pass_accuracy_away': 76.92,
            'fouls_committed_home': 12,
            'fouls_committed_away': 8,
            'corners_home': 4,
            'corners_away': 6,
            'yellow_cards_home': 2,
            'yellow_cards_away': 1,
            'red_cards_home': 0,
            'red_cards_away': 1,
            'offsides_home': 2,
            'offsides_away': 1,
            'saves_home': 3,
            'saves_away': 4
        }

        statistics_generator.publish_statistics(statistics)

        mock_producer.produce.assert_called_once_with("statistics", value=json.dumps(statistics))

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app_client.test_client()

    # @patch('app.get_recommendation_coupon', MagicMock(return_value={
    #         "coupon_id": "87a74a51-8d4d-4ecf-a5b5-623042c8bb6b",
    #         "selections": [
    #             {
    #                 "event_id": "d89aa157-efc6-481a-a2aa-1c615d9a9f62",
    #                 "odds": 1.67
    #             }
    #         ],
    #         "stake": 15.0,
    #         "timestamp": "2023-04-30T12:00:00Z",
    #         "user_id": 5
    #
    #     }))
    # def test_get_recommendation_1(self):
    #     payload = {"user_id": 1, "generator": "random"}
    #     response = self.client.post('/recommend', json=payload)
    #
    #     mocked_registry = {
    #         "dummy": recommendations.dummy_generator,
    #         "random": recommendations.random_generator,
    #     }
    #
    #     recommendation = app.get_recommendation_coupon.return_value
    #
    #     app.get_recommendation_coupon.assert_called_once_with(mocked_registry, "random", 1)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.is_json)
    #     self.assertEqual(response.json, recommendation)
    #
    # @patch('app.get_recommendation_coupon', MagicMock(return_value={
    #         "coupon_id": "8bcc0f90-96e9-4f87-aeab-22aff8c278ae",
    #         "selections": [
    #             {
    #                 "event_id": "7099151a-33aa-423f-9915-225c07c1daca",
    #                 "odds": 3.97
    #             },
    #             {
    #                 "event_id": "f597d516-d3cf-47cc-82dc-f9f4b03a6589",
    #                 "odds": 2.9
    #             },
    #             {
    #                 "event_id": "e6386e08-dafe-4f3e-9702-b1955eef03a7",
    #                 "odds": 4.91
    #             }
    #         ],
    #         "stake": 40.8,
    #         "timestamp": "2020-01-01101:05:01",
    #         "user_id": 1
    #     }))
    # def test_get_recommendation_2(self):
    #     payload = {"user_id": 2, "generator": "dummy"}
    #     response = self.client.post('/recommend', json=payload)
    #
    #     mocked_registry = {
    #         "dummy": recommendations.dummy_generator,
    #         "random": recommendations.random_generator,
    #     }
    #
    #     recommendation = app.get_recommendation_coupon.return_value
    #
    #     app.get_recommendation_coupon.assert_called_once_with(mocked_registry, "dummy", 2)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.is_json)
    #     self.assertEqual(response.json, recommendation)


if __name__ == '__main__':
    unittest.main()