from fastapi import Depends, HTTPException
from app.auth.dependencies import get_auth_crud
from app.auth.crud import AuthCRUD
from app.auth.schemas import UserCreate, UserBase, AuthLogin
from app.auth.password import get_password_hash, verify_password
from app.auth.jwt import JWTBackend
from app.core.error_messages import get_error_message


class AuthService:
    def __init__(self, crud: AuthCRUD = Depends(get_auth_crud)):
        self.crud = crud
        self.jwt = JWTBackend()

    async def register(self, data: UserCreate) -> tuple[dict, UserBase]:
        if await self._email_exists(data.email):
            raise HTTPException(400, detail=get_error_message("existing email"))
        # if await self._username_exists(data.username):
        #     raise HTTPException(400, detail=get_error_message("existing username"))
        hashed_password = get_password_hash(data.password)
        user_base = await self.crud.create(data, hashed_password)
        # asyncio.create_task(self._request_email_confirmation(new_user.email))
        tokens = self.jwt.create_tokens(user_base.dict())
        return tokens, user_base

    async def login(self, data: AuthLogin, ip: str) -> dict:
        """POST /login
        Args:
            data: AuthLogin
            ip: for bruteforce check.
        Returns:
            Access, refresh tokens and claims.
        Raises:
            HTTPException:
                400 - validation error or ban.
                404 - user doesn't exist.
                429 - bruteforce attempt.
        """
        # if await self._is_bruteforce(ip, user.email):
        #     raise HTTPException(429, detail="Too many requests")

        user = await self.crud.get_by_email(data.email)

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(401, detail="credential invalid")

        # await self._update_last_login(user.get("id"))
        user_base = UserBase.from_orm(user)
        tokens = self.jwt.create_tokens(user_base.dict())
        return tokens

    async def _email_exists(self, email: str) -> bool:
        """
        Check if email exists.
        Args:
            email (str): email.
        Returns:
            bool: True if email exists.
        """
        return await self.crud.verify_email(email)

    async def refresh_access_token(self, refresh_token: str) -> str:
        """POST /token/refresh

        Args:
            refresh_token: refresh_token from cookies.

        Returns:
            Access token.

        Raises:
            HTTPException:
                401 - type != refresh or ban.
                500 - ttt
        """
        refresh_token_payload = await self.jwt.decode_token(refresh_token)
        if (
            refresh_token_payload is None
            or refresh_token_payload.get("type") != "refresh"
        ):
            raise HTTPException(401)

        user = await self.crud.get_by_email(refresh_token_payload.get("email"))
        if user is None or not user.is_active:
            raise HTTPException(401)

        payload = item.dict(include={'username', 'email', 'id'})
        return self._auth_backend.create_access_token(payload)
