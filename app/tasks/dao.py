from datetime import date
from app.tasks.models import Task
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession



class TaskDAO:
    @classmethod
    async def create_task(cls, db: AsyncSession, task: Task) -> Task:
        new_task = Task(**task, created_at=date.today())
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task
    

    @classmethod
    async def get_all_tasks(cls, db: AsyncSession, complete: bool, user_id: int) -> list[Task]:
        query = select(Task).filter_by(complete=complete, user_id=user_id) if complete is not None else select(Task).filter_by(user_id=user_id)
        result = await db.execute(query)
        return result.scalars().all()


    @classmethod
    async def get_task_by_id(cls, task_id: int, db: AsyncSession, user_id: int) -> Task:
        query = select(Task).filter_by(id=task_id, user_id=user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    

    @classmethod
    async def update_task_by_id(cls, task_id: int, db: AsyncSession, update_data: Task) -> Task:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        if task:
            for key, value in update_data.items():
                setattr(task, key, value)
            db.add(task)
            await db.commit()
            await db.refresh(task)
        return task


    @classmethod
    async def delete_task_by_id(cls, task_id: int, db: AsyncSession, user_id: int) -> bool:
        query = select(Task).filter_by(Task.id == task_id, user_id=user_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        if task:
            await db.delete(task)
            await db.commit()
            return True
        return False