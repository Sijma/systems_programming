import os
import psycopg2
import schemas

query_registry = {
    schemas.TYPE_USER: "INSERT INTO users (user_id, birth_year, country, currency, gender, registration_date) VALUES (%s, %s, %s, %s, %s, %s)",
    schemas.TYPE_EVENT: "INSERT INTO events (event_id, begin_timestamp, end_timestamp, country, league, participants, sport) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    schemas.TYPE_COUPON: "" # TODO
}

unpack_registry = {
    schemas.TYPE_USER: lambda user_json: (user_json["user_id"], user_json["birth_year"], user_json["country"], user_json["currency"], user_json["gender"], user_json["registration_date"]),
    schemas.TYPE_EVENT: lambda event_json: (event_json['event_id'], event_json['begin_timestamp'], event_json['end_timestamp'], event_json['country'], event_json['league'], event_json['participants'], event_json['sport']),
    schemas.TYPE_COUPON: lambda coupon_json: None # TODO
}

conn = psycopg2.connect(
    host=os.environ.get('POSTGRES_HOST'),
    port=os.environ.get('POSTGRES_PORT'),
    dbname=os.environ.get('POSTGRES_DB'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_HOST')
)

def insert_one(data_json, data_type):
    schemas.validate(data_json, schemas.schema_registry[data_type])
    cur = conn.cursor()
    query = query_registry[data_type]
    data = unpack_registry[data_type](data_json)
    cur.execute(query, data)
