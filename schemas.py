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