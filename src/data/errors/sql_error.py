from enum import Enum, auto


class SQLError(Enum):
    duplicate_entry = auto()
    unique_constraint = auto()
    not_found = auto()

