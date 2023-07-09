import os
import psycopg2

TYPE_USER = "user"
TYPE_EVENT = "event"
TYPE_COUPON = "coupon"
TYPE_STATISTICS = "statistics"

table_registry = {
    TYPE_USER: "users",
    TYPE_EVENT: "events",
    TYPE_COUPON: "coupons",
    TYPE_STATISTICS: "historical_events"
}


def construct_query(json_data, data_type, batch=False):
    table_name = table_registry[data_type]

    if not batch:
        json_data = [json_data]

    first_json = json_data[0]
    keys = list(first_json.keys())
    values = []

    for record in json_data:
        values.append(tuple(record[key] for key in keys))

    placeholders = ', '.join(['%s'] * len(keys))

    query = f"INSERT INTO {table_name} ({', '.join(keys)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

    if not batch:
        values = values[0]

    return query, values

class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=25,  # min = number of connections initially created
                maxconn=50,
                host=os.environ.get('POSTGRES_HOST'),
                port=os.environ.get('POSTGRES_PORT'),
                dbname=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
        return cls._instance

    class DatabaseConnectionManager:
        def __enter__(self):
            self.conn = Database._instance.connection_pool.getconn()
            self.cur = self.conn.cursor()
            return self.cur

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.cur.close()
            Database._instance.connection_pool.putconn(self.conn)

    def insert(self, data_json, data_type, batch=False):
        with self.DatabaseConnectionManager() as cur:
            query, data = construct_query(data_json, data_type, batch)
            if batch:
                cur.executemany(query, data) # TODO: Consider using fast_executemany. Apparently executemany is just a loop of execute which is bad for performance
            else:
                cur.execute(query, data)

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
        with self.DatabaseConnectionManager() as cur:
            cur.execute(query)

            result = cur.fetchone()

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
        with self.DatabaseConnectionManager() as cur:
            cur.execute(query, (coupon_timestamp,))
            result = cur.fetchone()
            event_id = result[0] if result else None
            return event_id
    def get_random_user_id(self):
        query = "SELECT user_id FROM users ORDER BY random() LIMIT 1"
        with self.DatabaseConnectionManager() as cur:
            cur.execute(query)
            result = cur.fetchone()
            user_id = result[0] if result else None
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
        with self.DatabaseConnectionManager() as cur:
            cur.execute(query, (amount,))
            return cur.fetchall()