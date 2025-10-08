from enum import Enum, auto


class RedisError(Enum):
    nonexistent_key = auto()
    key_without_expiration = auto()

