from database import Database
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError, BaseModel

app = FastAPI()
db = Database()

class InsertPayload(BaseModel):
    data_json: list
    data_type: str
    batch: bool = False

@app.get("/")
def status():
    return {"Status", "UP"}

@app.post("/insert")
def insert_data(payload: InsertPayload):
    db.insert(payload.data_json, payload.data_type, payload.batch)
    return {"message": "Data inserted successfully"}


@app.get("/random_event/statistics")
def get_random_event_id_for_statistics():
    event_id = db.get_random_event_id_for_statistics()
    return {"event_id": event_id}


@app.get("/random_event/{coupon_timestamp}")
def get_random_event_id_after_timestamp(coupon_timestamp: str):
    event_id = db.get_random_event_id_after_timestamp(coupon_timestamp)
    return {"event_id": event_id}


@app.get("/random_user")
def get_random_user_id():
    user_id = db.get_random_user_id()
    return {"user_id": user_id}


@app.get("/most_played_events/{amount}")
def get_most_played_events(amount: int):
    events = db.get_most_played_events(amount)
    return {"events": events}
