from dataclasses import dataclass
from uuid import UUID
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exeception import TaskNotFound
from app.models import TaskModel, TaskStatus
from app.schema.task import TaskCreateSchema


@dataclass
class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_task(self, task_create_schema: TaskCreateSchema) -> UUID:
        task_model = TaskModel(search_queries=task_create_schema.search_queries)
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            return task_model.id

    async def get_task(self, task_id: UUID) -> TaskModel | None:
        query = select(TaskModel).where(TaskModel.id == task_id)
        async with self.db_session as session:
            task: TaskModel = (await session.execute(query)).scalar_one_or_none()
        if not task: raise TaskNotFound
        return task

    async def get_tasks_all(self) -> list[TaskModel] | None:
        query = select(TaskModel)
        async with self.db_session as session:
            tasks: list[TaskModel] = list((await session.execute(query)).scalars().all())
        return tasks

    async def delete_task(self, task_id: UUID):
        query = delete(TaskModel).where(TaskModel.id == task_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def update_task_status(self, task_id: UUID, status: str):
        query = (
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(status=status)
        )
        await self.db_session.execute(query)
        await self.db_session.commit()