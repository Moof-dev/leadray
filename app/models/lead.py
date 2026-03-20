from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class LeadModel(Base):
    __tablename__ = "leads"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"))
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=True)

    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Сделаем nullable
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)  # Убрал unique

    profile_url: Mapped[str | None] = mapped_column(String(500), index=True, nullable=True)

    additional_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    task: Mapped["TaskModel"] = relationship(back_populates="leads")
    company: Mapped["CompanyModel"] = relationship(back_populates="leads")