from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LeadModel
from app.schema import LeadCreateSchema


@dataclass
class LeadRepository:
    db_session: AsyncSession

    async def add_leads_bulk(self, leads: list[LeadCreateSchema]):
        if not leads:
            return

        data = [lead.model_dump() for lead in leads]
        query = insert(LeadModel).values(data)

        await self.db_session.execute(query)
        await self.db_session.commit()

    async def add_lead(self, lead: LeadCreateSchema):
        lead_model = LeadModel(**lead.model_dump())
        self.db_session.add(lead_model)
        await self.db_session.commit()
        await self.db_session.refresh(lead_model)
        return lead_model