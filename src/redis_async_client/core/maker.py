from typing import AsyncGenerator

from redis import Redis
from redis import asyncio as redis

from src.redis_async_client import AsyncRedisClient, RedisSettings


async def get_redis() -> AsyncGenerator[Redis, None]:
    pool = RedisSettings().make_pool()
    redis_client: Redis = redis.Redis(connection_pool=pool)
    yield redis_client
    await redis_client.close()


async def get_redis_client() -> AsyncGenerator[AsyncRedisClient, None]:
    async for client in get_redis():
        yield AsyncRedisClient(client)


async def check_redis_connection():
    async for client in get_redis_client():
        await client.health_check()


async def get_redis_connection(
    redis_settings: RedisSettings,
) -> AsyncGenerator[AsyncRedisClient, None]:
    pool = redis_settings.make_pool()
    redis_client: Redis = redis.Redis(connection_pool=pool)
    yield AsyncRedisClient(redis_client)
    await redis_client.close()
