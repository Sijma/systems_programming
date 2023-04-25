def dummy(v):
    return {
        "recommendation": "dummy"
    }


def random(v):
    return {
        "recommendation": "random"
    }


recommendation_registry = {
        "dummy": dummy,
        "random": random,
    }


def get_recommendation_based_on_user_id(registry, user_id):
    if user_id % 2 == 0:
        return registry["dummy"](user_id)
    return registry["random"](user_id)
