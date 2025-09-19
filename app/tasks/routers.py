from fastapi import APIRouter, Depends, HTTPException
from app.tasks.schemas import TaskCreate, TaskInDBBase, TaskUpdate
from app.tasks.dao import TaskDAO
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


@router.post("/", response_model=TaskInDBBase)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    return await TaskDAO.create_task(task=task.model_dump(), db=db)


@router.get("/", response_model=list[TaskInDBBase])
async def get_tasks(db: AsyncSession = Depends(get_async_session), complete: bool | None = None, current_user: str = Depends(get_current_user)):
    return await TaskDAO.get_all_tasks(db=db, complete=complete, user_id=current_user)


@router.get("/{task_id}", response_model=TaskInDBBase)
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    task = await TaskDAO.get_task_by_id(task_id=task_id, db=db, user_id=current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskInDBBase)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: str = Depends(get_current_user)
):
    existing_task = await TaskDAO.get_task_by_id(task_id=task_id, db=db, user_id=current_user)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task.model_dump(exclude_unset=True)
    updated_task = await TaskDAO.update_task_by_id(task_id=task_id, update_data=update_data, db=db)
    return updated_task


@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)):
    success = await TaskDAO.delete_task_by_id(task_id=task_id, db=db, user_id=current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}