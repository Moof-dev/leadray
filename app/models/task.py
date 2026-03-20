from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, TaskStatus


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)
    search_queries: Mapped[dict] = mapped_column(JSON, nullable=True)
    leads_found: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Связь: одна задача может найти много лидов
    leads: Mapped[list["LeadModel"]] = relationship(back_populates="task")