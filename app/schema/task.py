from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models import TaskStatus


class TaskSchema(BaseModel):
    id: UUID
    status: TaskStatus
    search_queries: dict | None = None
    leads_found: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class TaskCreateSchema(BaseModel):
    search_queries: dict | None = None
