from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.cache import RedisBackend
from app import settings


pwd_context = CryptContext(schemes=['bcrypt'])
JWT_ALGORITHM = "HS256"


class JWTBackend:
    """
    Setup the JWT Backend with the given cache backend and private key.
    """
    _private_key = settings.private_key
    _access_expiration = settings.access_expiration
    _refresh_expiration = settings.refresh_expiration

    def __init__(self, cache: RedisBackend = Depends(RedisBackend)):
        self._cache = cache

    def _create_token(self, payload: dict, token_type: str, expiration_delta: int = 600):
        """Cria um token

        :payload: um dict do tipo
            { "sub": email }
        :return token_jwt
        """
        payload = payload.copy()
        iat = datetime.utcnow()
        exp = datetime.utcnow() + timedelta(seconds=expiration_delta)

        payload.update({"iat": iat, "exp": exp, "type": token_type})
        token = jwt.encode(payload, self._private_key, algorithm=JWT_ALGORITHM)
        return token

    def create_access_token(self, payload: dict) -> str:
        return self._create_token(payload, "access", self._access_expiration)

    def create_refresh_token(self, payload: dict) -> str:
        return self._create_token(payload, "refresh", self._refresh_expiration)

    def create_tokens(self, payload: dict) -> dict:
        access = self.create_access_token(payload)
        refresh = self.create_refresh_token(payload)

        return {"access": access, "refresh": refresh, "claims": payload}

    async def _active_blackout_exists(self, iat: datetime) -> bool:
        blackout = await self._cache.get("users:blackout")
        if blackout is not None:
            blackout_ts = datetime.utcfromtimestamp(int(blackout))
            return blackout_ts >= iat
        else:
            return False

    async def _user_in_blacklist(self, id: int) -> bool:
        in_blacklist = await self._cache.get(f"users:blacklist:{id}")
        return bool(in_blacklist)

    async def _user_in_logout(self, id: int, iat: datetime) -> bool:
        ts = await self._cache.get(f"users:kick:{id}")
        if ts is not None:
            logout_ts = datetime.utcfromtimestamp(int(ts))
            return logout_ts >= iat
        else:
            return False

    async def decode_token(self, token: str):
        if token:
            try:
                payload = jwt.decode(
                    token,
                    self._private_key,
                    algorithms=JWT_ALGORITHM,
                )
                print(f"RESULTADO DO DECODE JWT PAYLOAD: {payload}")
                iat = datetime.utcfromtimestamp(int(payload.get("iat")))
                # checks = await asyncio.gather(
                #      *(
                #          self._active_blackout_exists(iat),
                #          self._user_in_blacklist(id),
                #          self._user_in_logout(id, iat),
                #      )
                #  )
                # if any(checks):
                #      return None

                return payload
            except:  # noqa E722
                return None
        return None
