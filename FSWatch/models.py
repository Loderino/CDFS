import enum

class EventType(enum.Enum):
    CREATED = 0
    MOVED = 1
    MODIFIED = 2
    DELETED = 3