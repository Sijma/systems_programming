recommendation_request_schema = {
    "type": "object",
    "properties": {
        "user-id": {"type": "integer"},
    },
    "required": ["user-id"]
}

recommendation_response_schema = {
    "type": "object",
    "properties": {
        "recommendation": {"type": "string"}
    },
    "required": ["recommendation"]
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

coupon = {
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
                        "multipleOf": 0.01
                    }
                }
            }
        },
        "stake": {
            "type": "number",
            "multipleOf": 0.01
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
