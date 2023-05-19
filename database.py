import psycopg2
import schemas
import config

conn = psycopg2.connect(
    dbname=config.database_name,
    user=config.username,
    password=config.password,
    host=config.host,
    port=config.port
)


# How do we unittest these? Do we create a test_database and create/delete tables within the context of each test?

# Maybe insert statements can be further abstracted into a single function, where the insert schema is an argument.
# however that's not straight forward with these strict query and data structures.
# The queries can easily be in a simple registry, but the json data needs to be properly unpacked, in specific order and regardless of content/key names.
def add_single_event(event_json):
    cur = conn.cursor()
    schemas.validate(event_json, schemas.event_schema)
    query = "INSERT INTO events (event_id, begin_timestamp, end_timestamp, country, league, participants, sport) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (event_json['event_id'], event_json['begin_timestamp'], event_json['end_timestamp'], event_json['country'], event_json['league'], event_json['participants'], event_json['sport'])
    cur.execute(query, data)
    conn.commit()
    cur.close()


def add_single_user(user_json):
    cur = conn.cursor()
    # schemas.validate(user_json, schemas.user_schema)
    query = "INSERT INTO users (birth_year, country, currency, gender, registration_date) VALUES (%s, %s, %s, %s, %s) RETURNING user_id"
    data = (user_json["birth_year"], user_json["country"], user_json["currency"], user_json["gender"], user_json["registration_date"])
    cur.execute(query, data)
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return user_id
