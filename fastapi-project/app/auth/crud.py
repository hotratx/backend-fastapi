from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.models import User
from app.auth.schemas import UserCreate, UserBase


class AuthCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate, hashed_password: str) -> UserBase:
        values = data.dict()

        hero = User(**values, hashed_password=hashed_password)
        self.session.add(hero)
        await self.session.commit()
        await self.session.refresh(hero)

        return UserBase.from_orm(hero)

    async def get(self, user_id: str | UUID) -> User:
        statement = select(User).where(User.uuid == user_id)
        results = await self.session.execute(statement=statement)
        hero = results.scalar_one_or_none()  # type: User | None

        if hero is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        return hero

    async def get_by_email(self, user_email: str) -> User:
        statement = select(User).where(User.email == user_email)
        results = await self.session.execute(statement=statement)
        user = results.scalar_one_or_none()  # type: User | None

        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        return user

    async def verify_email(self, user_email: str | UUID) -> bool:
        statement = select(User).where(User.email == user_email)
        results = await self.session.execute(statement=statement)
        user = results.scalar_one_or_none()  # type: User | None

        if user:
            return True
        return False



    async def delete(self, user_id: str | UUID) -> bool:
        statement = delete(User).where(User.uuid == user_id)
        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
