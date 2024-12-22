import enum

class EventType(enum.Enum):
    """Enumeration for different types of file system events.

    Attributes:
        CREATED (int): Event type for a newly created file.
        MOVED (int): Event type for a file that has been moved.
        MODIFIED (int): Event type for a file that has been modified.
        DELETED (int): Event type for a file that has been deleted.
    """
    CREATED = 0
    MOVED = 1
    MODIFIED = 2
    DELETED = 3
