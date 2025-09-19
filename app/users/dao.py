from app.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserDAO:
    @classmethod
    async def create_user(cls, db: AsyncSession, **user) -> User:
        new_user = User(**user)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str) -> User:
        query = select(User).where(User.email == email)
        user = await db.execute(query)
        return user.scalar_one_or_none()
    

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, id: int) -> User:
        query = select(User).where(User.id == id)
        user = await db.execute(query)
        return user.scalar_one_or_none()