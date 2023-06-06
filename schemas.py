from functools import wraps

from flask import request, jsonify
from jsonschema import validate, ValidationError

TYPE_USER = "user"
TYPE_EVENT = "event"
TYPE_COUPON = "coupon"
TYPE_STATISTICS = "statistics"

recommendation_request_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "integer", "minimum": 1},
        "generator": {"type": "string", "enum": ["dummy", "random", "popular"]},
        "amount": {"type": "integer", "minimum": 1},
    },
    "required": ["user_id", "generator", "amount"],
    "additionalProperties": False
}

user_schema = {
    "type": "object",
    "properties": {
        "birth_year": {
            "type": "integer",
            "minimum": 1900,
            "maximum": 2023
        },
        "country": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
        },
        "currency": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
        },
        "gender": {
            "type": "string",
            "enum": [
                "Male",
                "Female",
                "Other"
            ]
        },
        "registration_date": {
            "type": "string",
            "format": "date-time"
        },
        "user_id": {
            "type": "integer",
            "minimum": 1
        }
    },
    "required": [
        "birth_year",
        "country",
        "currency",
        "gender",
        "registration_date",
        "user_id"
    ],
    "additionalProperties": False
}

event_schema = {
    "type": "object",
    "properties": {
        "begin_timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "country": {
            "type": "string"
        },
        "end_timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "event_id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
            # This is a regex (regular expression) for UUID (Universally unique identifier)
        },
        "league": {
            "type": "string"
        },
        "home_team": {
            "type": "string"
        },
        "away_team": {
            "type": "string"
        }
    },
    "required": [
        "begin_timestamp",
        "country",
        "end_timestamp",
        "event_id",
        "league",
        "home_team",
        "away_team"
    ],
    "additionalProperties": False
}

coupon_schema = {
    "type": "object",
    "properties": {
        "coupon_id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
            # This is a regex (regular expression) for UUID (Universally unique identifier)
        },
        "selections": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "event_id",
                    "outcome",
                    "odds"
                ],
                "properties": {
                    "event_id": {
                        "type": "string",
                        "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
                        # This is a regex (regular expression) for UUID (Universally unique identifier)
                    },
                    "outcome": {
                        "type": "string",
                        "enum": ["home win", "away win", "draw"]
                    },
                    "odds": {
                        "type": "number",
                    }
                },
                "additionalProperties": False
            }
        },
        "stake": {
            "type": "number",
            "minimum": 1.0
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "user_id": {
            "type": "integer",
            "minimum": 1
        }
    },
    "required": [
        "coupon_id",
        "selections",
        "stake",
        "timestamp",
        "user_id"
    ],
    "additionalProperties": False
}

statistics_schema = {
    "type": "object",
    "properties": {
        "event_id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        },
        "result": {
            "type": "string",
            "enum": ["home win", "away win", "draw"]
        },
        "goals_scored_home": {
            "type": "integer"
        },
        "goals_scored_away": {
            "type": "integer"
        },
        "shots_on_target_home": {
            "type": "integer"
        },
        "shots_on_target_away": {
            "type": "integer"
        },
        "total_shots_home": {
            "type": "integer"
        },
        "total_shots_away": {
            "type": "integer"
        },
        "possession_percentage_home": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
        },
        "possession_percentage_away": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
        },
        "pass_accuracy_home": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
        },
        "pass_accuracy_away": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
        },
        "fouls_committed_home": {
            "type": "integer"
        },
        "fouls_committed_away": {
            "type": "integer"
        },
        "corners_home": {
            "type": "integer"
        },
        "corners_away": {
            "type": "integer"
        },
        "yellow_cards_home": {
            "type": "integer"
        },
        "yellow_cards_away": {
            "type": "integer"
        },
        "red_cards_home": {
            "type": "integer"
        },
        "red_cards_away": {
            "type": "integer"
        },
        "offsides_home": {
            "type": "integer"
        },
        "offsides_away": {
            "type": "integer"
        },
        "saves_home": {
            "type": "integer"
        },
        "saves_away": {
            "type": "integer"
        }
    },
    "required": [
        "event_id",
        "result",
        "goals_scored_home",
        "goals_scored_away",
        "shots_on_target_home",
        "shots_on_target_away",
        "total_shots_home",
        "total_shots_away",
        "possession_percentage_home",
        "possession_percentage_away",
        "pass_accuracy_home",
        "pass_accuracy_away",
        "fouls_committed_home",
        "fouls_committed_away",
        "corners_home",
        "corners_away",
        "yellow_cards_home",
        "yellow_cards_away",
        "red_cards_home",
        "red_cards_away",
        "offsides_home",
        "offsides_away",
        "saves_home",
        "saves_away"
    ],
    "additionalProperties": False
}

schema_registry = {
    TYPE_USER: user_schema,
    TYPE_EVENT: event_schema,
    TYPE_COUPON: coupon_schema,
    TYPE_STATISTICS: statistics_schema
}


# No idea how to unittest this, nor integrate test in the flask view
def json_validator(schema):  # Decorator factory, returns decorator function
    def decorator(f):  # f argument here is our "view", which is the app.route function we're decorating this with. It returns a "wrapped" view function, which adds the wrapper code to our original function.
        @wraps(f)  # @wraps is used to preserve the original name and docstring of the view function being decorated
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"message": "Invalid request body: expected JSON"}), 400
            try:
                validate(request.json, schema)  # Should the validation be in a separate function?
            except ValidationError as e:
                return jsonify({"message": str(e)}), 400
            return f(*args, **kwargs)  # We route the view response to the decorator's wrapper again to validate it too
        return wrapper
    return decorator
