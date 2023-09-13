from abc import ABC, abstractmethod


class Recommender(ABC):
    _registry = {}

    def __init_subclass__(cls, cl_name=None):
        if cl_name:
            cls._registry[cl_name] = cls

    @classmethod
    def register(cls, name, subclass):
        cls._registry[name] = subclass

    @classmethod
    def get_recommender(cls, name):
        return cls._registry.get(name)

    @classmethod
    def get_recommender_func(cls, name):
        return cls._registry.get(name).recommend

    @classmethod
    @abstractmethod
    def recommend(cls, user_id, recommendation_amount):
        pass


# def register_recommender(name):
#     def decorator(subclass):
#         Recommender.register(name, subclass)
#         return subclass
#     return decorator
