from typing import Iterable, Union
import aioredis
from app import settings


class RedisBackend:
    """
    Setup the Redis connection for the backend using aioredis.
    """
    _redis = aioredis.from_url(settings.url_cache)

    async def get(self, key: str):
        return await self._redis.get(key)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)
        return None

    async def keys(self, match: str) -> Iterable[str]:
        return await self._redis.keys(match)

    async def set(
        self, key: str, value: Union[str, bytes, int], ex: int = 0
    ) -> None:
        await self._redis.set(key, value)
        return None

    async def setnx(self, key: str, value: Union[str, bytes, int], expire: int) -> None:
        await self._redis.setnx(key, value)
        await self._redis.expire(key, expire)
        return None

    async def incr(self, key: str) -> str:
        return await self._redis.incr(key)

    async def dispatch_action(self, channel: str, action: str, payload: dict) -> None:
        await self._redis.publish_json(channel, {"action": action, "payload": payload})
        return None
