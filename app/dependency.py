from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.db.session import get_db_session
from app.repository import TaskRepository
from app.services.tasks import TaskService


async def get_task_repository(db_session: AsyncSession = Depends(get_db_session)):
    return TaskRepository(db_session=db_session)

async def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository)
):
    return TaskService(task_repository=task_repository)




