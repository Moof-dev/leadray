from uuid import UUID, uuid4
from sqlalchemy import  String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class CompanyModel(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    domain: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    industry: Mapped[str] = mapped_column(String(255), nullable=True)
    size_range: Mapped[str] = mapped_column(String(50), nullable=True)
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=True)

    leads: Mapped[list["LeadModel"]] = relationship(back_populates="company")