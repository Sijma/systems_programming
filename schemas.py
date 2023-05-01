from functools import wraps
from jsonschema import validate, ValidationError
from recommendations import recommendation_registry
from flask import request, jsonify

recommendation_request_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "integer", "minimum": 1},
        "generator": {"type": "string", "enum": list(recommendation_registry.keys())}
    },
    "required": ["user_id", "generator"]
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
    ]
}

event_schema = {
    "type": "object",
    "properties": {
        "begin_timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "country": {
            "type": "string",
            "pattern": "^[A-Z]{3}$"
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
        "participants": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 2,
            "maxItems": 2
            # To ensure we have exactly 2 participants
        },
        "sport": {
            "type": "string",
        }
    },
    "required": [
        "begin_timestamp",
        "country",
        "end_timestamp",
        "event_id",
        "league",
        "participants",
        "sport"
    ]
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
                    "odds"
                ],
                "properties": {
                    "event_id": {
                        "type": "string",
                        "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
                        # This is a regex (regular expression) for UUID (Universally unique identifier)
                    },
                    "odds": {
                        "type": "number",
                    }
                }
            }
        },
        "stake": {
            "type": "number",
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
    ]
}


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
            return f(*args, **kwargs)
        return wrapper
    return decorator
