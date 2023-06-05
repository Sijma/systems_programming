import os
import json
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool
import schemas

query_registry = {
    schemas.TYPE_USER: "INSERT INTO users (user_id, birth_year, country, currency, gender, registration_date) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
    schemas.TYPE_EVENT: "INSERT INTO events (event_id, begin_timestamp, end_timestamp, country, league, participants, sport) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
    schemas.TYPE_COUPON: "INSERT INTO coupons (coupon_id, selections, stake, timestamp, user_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
}

unpack_registry = {
    schemas.TYPE_USER: lambda user_json: (user_json['user_id'], user_json['birth_year'], user_json['country'], user_json['currency'], user_json['gender'], user_json['registration_date']),
    schemas.TYPE_EVENT: lambda event_json: (event_json['event_id'], event_json['begin_timestamp'], event_json['end_timestamp'], event_json['country'], event_json['league'], event_json['participants'], event_json['sport']),
    schemas.TYPE_COUPON: lambda coupon_json: (coupon_json['coupon_id'], json.dumps(coupon_json['selections']),coupon_json['stake'],coupon_json['timestamp'],coupon_json['user_id'])
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

    @contextmanager
    def database_connection(self):
        conn = self.connection_pool.getconn()
        try:
            yield conn # Yield can be used produce/dynamically generate something like a lazy-evaluated iterable
            conn.commit()
        finally:
            self.connection_pool.putconn(conn)

    def batch_unpack(self, data_json, data_type):
        unpack_function = unpack_registry[data_type]
        data_list = [unpack_function(record) for record in data_json]
        return data_list

    def insert(self, data_json, data_type, batch=False):
        with self.database_connection() as conn:
            cur = conn.cursor() # TODO: Consider handling the cursor using a context block (with:)
            query = query_registry[data_type]
            if batch:
                data = self.batch_unpack(data_json, data_type)
                cur.executemany(query, data) # TODO: Consider using fast_executemany. Apparently executemany is just a loop of execute which is bad for performance
            else:
                data = unpack_registry[data_type](data_json)
                cur.execute(query, data)
            cur.close()

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
        with self.database_connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchone()

            # If an eligible event_id is found, return it; otherwise, return None
            event_id = result[0] if result else None
            return event_id