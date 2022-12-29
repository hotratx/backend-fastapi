from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.auth.crud import AuthCRUD
from app.auth.jwt import JWTBackend


oauth2_schema = APIKeyCookie(name="access_token")


async def get_auth_crud(
        session: AsyncSession = Depends(get_async_session)
) -> AuthCRUD:
    return AuthCRUD(session=session)


async def get_authenticated_user(
        jwt: JWTBackend = Depends(JWTBackend),
        crud: AuthCRUD = Depends(get_auth_crud),
        token: str = Depends(oauth2_schema)
):
    if token:
        data = await jwt.decode_token(token)
        user = await crud.get_by_email(data["email"])
        return user
    else:
        raise HTTPException(401)
