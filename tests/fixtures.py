import asyncio

import pytest
import redis.asyncio as redis

from src.redis_async_client import RedisSettings


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope='session')
def redis_test_settings() -> RedisSettings:
    return RedisSettings()


@pytest.fixture(scope='session')
def redis_test_pool(
    redis_test_settings: RedisSettings,
) -> redis.ConnectionPool:
    return redis_test_settings.make_pool()


@pytest.fixture(scope='session')
async def redis_test_instance(
    redis_test_pool: redis.ConnectionPool,
):
    instance = redis.Redis(connection_pool=redis_test_pool)
    yield instance
    await instance.close()
