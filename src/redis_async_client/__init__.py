from typing import AsyncGenerator

from redis import asyncio as redis_async

from .core.async_client import AsyncRedisClient
from .core.exc import RedisAsyncClientException
from .core.settings import RedisSettings


__all__ = (
    "AsyncRedisClient",
    "RedisSettings",
    "RedisAsyncClientException",
    "get_redis_connection",
)


async def get_redis_connection(
    redis_settings: RedisSettings,
) -> AsyncGenerator[AsyncRedisClient, None]:
    pool: redis_async.ConnectionPool = redis_settings.make_pool()
    async with redis_async.Redis(connection_pool=pool) as conn:
        async_client = AsyncRedisClient(conn)
        yield async_client
