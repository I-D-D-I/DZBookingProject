from enum import Enum


class Environment(Enum):
    TEST = 'production'
    PROD = 'test'
    # TEST = 'test'
    # PROD = 'production'