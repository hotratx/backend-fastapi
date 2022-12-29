from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.auth.crud import AuthCRUD


async def get_auth_crud(
        session: AsyncSession = Depends(get_async_session)
) -> AuthCRUD:
    return AuthCRUD(session=session)
