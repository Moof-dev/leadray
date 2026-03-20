import enum

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class TaskStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"