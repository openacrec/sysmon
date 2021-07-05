from enum import Enum


class TaskStatus(Enum):
    """Statuses for the task execution process"""
    # if we can somewhat reliably gather a status
    COPYING = -1
    RUNNING = -1
    FINISHED = 0
    FAILED = 1
    UNKNOWN = None
