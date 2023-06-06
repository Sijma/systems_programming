import os
import json
import psycopg2
from psycopg2 import pool

TYPE_USER = "user"
TYPE_EVENT = "event"
TYPE_COUPON = "coupon"
TYPE_STATISTICS = "statistics"

query_registry = {
    TYPE_USER: "INSERT INTO users (user_id, birth_year, country, currency, gender, registration_date) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
    TYPE_EVENT: "INSERT INTO events (event_id, begin_timestamp, end_timestamp, country, league, home_team, away_team) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
    TYPE_COUPON: "INSERT INTO coupons (coupon_id, selections, stake, timestamp, user_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
}

unpack_registry = {
    TYPE_USER: lambda user_json: (user_json['user_id'], user_json['birth_year'], user_json['country'], user_json['currency'], user_json['gender'], user_json['registration_date']),
    TYPE_EVENT: lambda event_json: (event_json['event_id'], event_json['begin_timestamp'], event_json['end_timestamp'], event_json['country'], event_json['league'], event_json['home_team'], event_json['away_team']),
    TYPE_COUPON: lambda coupon_json: (coupon_json['coupon_id'], json.dumps(coupon_json['selections']),coupon_json['stake'],coupon_json['timestamp'],coupon_json['user_id'])
}

class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=5,  # min = number of connections initially created
                maxconn=10,
                host=os.environ.get('POSTGRES_HOST'),
                port=os.environ.get('POSTGRES_PORT'),
                dbname=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
        return cls._instance

    def __enter__(self):
        self.conn = self.connection_pool.getconn()
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cur.close()
        self.connection_pool.putconn(self.conn)

    def batch_unpack(self, data_json, data_type):
        unpack_function = unpack_registry[data_type]
        data_list = [unpack_function(record) for record in data_json]
        return data_list

    def insert(self, data_json, data_type, batch=False):
        with self:
            query = query_registry[data_type]
            if batch:
                data = self.batch_unpack(data_json, data_type)
                self.cur.executemany(query, data) # TODO: Consider using fast_executemany. Apparently executemany is just a loop of execute which is bad for performance
            else:
                data = unpack_registry[data_type](data_json)
                self.cur.execute(query, data)

    def get_random_event_id_for_statistics(self):
        query = """
                SELECT event_id
                FROM events
                WHERE end_timestamp < NOW()
                    AND event_id NOT IN (
                        SELECT event_id
                        FROM historical_events
                    )
                ORDER BY random()
                LIMIT 1
            """
        with self:
            self.cur.execute(query)
            result = self.cur.fetchone()

            # If an eligible event_id is found, return it; otherwise, return None
            event_id = result[0] if result else None
            return event_id

    def get_random_event_id_after_timestamp(self, coupon_timestamp):
        query = """
            SELECT event_id
            FROM events
            WHERE begin_timestamp > %s
            ORDER BY random()
            LIMIT 1
        """
        with self:
            self.cur.execute(query, (coupon_timestamp,))
            result = self.cur.fetchone()
            event_id = result[0] if result else None
            return event_id
    def get_random_user_id(self):
        query = "SELECT user_id FROM users ORDER BY random() LIMIT 1"
        with self:
            self.cur.execute(query)
            result = self.cur.fetchone()
            user_id = result[0]
            return user_id

    def get_most_played_events(self, amount):
        query = """
            SELECT e.event_id, s.selection ->> 'outcome' AS outcome, COUNT(*) AS appearances
            FROM events e
            INNER JOIN (
                SELECT s.selection
                FROM coupons c, jsonb_array_elements(c.selections) AS s(selection)
            ) AS s ON s.selection ->> 'event_id' = e.event_id::text
            GROUP BY e.event_id, outcome
            ORDER BY appearances DESC
            LIMIT %s;
        """
        with self:
            self.cur.execute(query, (amount,))
            return self.cur.fetchall()