from dataclasses import dataclass
from pydantic import TypeAdapter
from uuid import UUID

from app.repository import TaskRepository
from app.schema import TaskCreateSchema, TaskSchema
from app.worker.tasks import process_parsing


@dataclass
class TaskService:
    task_repository: TaskRepository


    async def create_task(
            self, task_create_schema: TaskCreateSchema
    ):
        task_id = await self.task_repository.create_task(task_create_schema=task_create_schema)
        task = TaskSchema.model_validate(await self.task_repository.get_task(task_id=task_id))
        process_parsing.delay(task_id=task.id, search_queries=task.search_queries)
        return task

    async def get_task(
            self, task_id: UUID
    ) -> TaskSchema:
        task = TaskSchema.model_validate(await self.task_repository.get_task(task_id=task_id))
        return task

    async def get_tasks_all(self) -> list[TaskSchema]:
        tasks_models = await self.task_repository.get_tasks_all()
        return TypeAdapter(list[TaskSchema]).validate_python(tasks_models)

    async def delete_task(self, task_id: UUID):
        await self.task_repository.delete_task(task_id)