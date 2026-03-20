from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from app.dependency import get_task_service
from app.exeception import TaskNotFound

from app.schema import TaskSchema, TaskCreateSchema
from app.services import TaskService


router = APIRouter(prefix="/task", tags=["task"])



@router.post("/", response_model=TaskSchema)
async def create_task(
        body: TaskCreateSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)]
) -> TaskSchema:
    return await task_service.create_task(body)

@router.get("/all")
async def get_tasks_all(
        task_service: Annotated[TaskService, Depends(get_task_service)]
) -> list[TaskSchema]:
    try:
        return await task_service.get_tasks_all()
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        task_id: UUID,
        task_service: Annotated[TaskService, Depends(get_task_service)]
) -> TaskSchema:
    try:
        return await task_service.get_task(task_id=task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: UUID,
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    await task_service.delete_task(task_id=task_id)