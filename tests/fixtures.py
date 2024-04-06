import asyncio

import pytest

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
