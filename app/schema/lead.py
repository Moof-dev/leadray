from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models import TaskStatus



class LeadBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    job_title: str | None = None
    email: str | None = None
    profile_url: str | None = None
    additional_data: dict | None = None

class LeadCreateSchema(LeadBase):
    task_id: UUID
    company_id: UUID | None = None

class LeadSchema(LeadBase):
    id: UUID
    task_id: UUID
    company_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)