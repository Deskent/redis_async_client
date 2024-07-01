import pytest
import redis.asyncio as redis_async

from src.redis_async_client import (
    AsyncRedisClient,
    RedisSettings,
    get_redis_connection,
)


KEY: str = 'test_key'


async def test_redis_health_check():
    redis_settings = RedisSettings()
    pool: redis_async.ConnectionPool = redis_settings.make_pool()
    async with redis_async.Redis(connection_pool=pool) as conn:
        async_client = AsyncRedisClient(conn)
        data = await async_client.health_check()
        assert data == {'test': 'test'}


async def test_get_redis_connection(redis_test_settings: RedisSettings):
    async for client in get_redis_connection(redis_test_settings):
        data = await client.health_check()
        assert data == {'test': 'test'}


async def test_update_method(redis_test_settings: RedisSettings):
    async for client in get_redis_connection(redis_test_settings):
        data = {'test': 'test'}
        await client.save(KEY, data)
        update_data: dict = {'update_key': 'test_updated_data'}
        await client.update(KEY, update_data)
        result: dict = await client.load(KEY)
        assert result == {'test': 'test', 'update_key': 'test_updated_data'}


async def test_append_method(redis_test_settings: RedisSettings):
    async for client in get_redis_connection(redis_test_settings):
        data = [1, 2, 3]
        await client.save(KEY, data)
        append_data: int = 4
        await client.append(KEY, append_data)
        result: dict = await client.load(KEY)
        assert result == [1, 2, 3, 4]


async def test_extend_method(redis_test_settings: RedisSettings):
    async for client in get_redis_connection(redis_test_settings):
        await client.delete(KEY)
        data = [1, 2, 3]
        await client.extend(KEY, data)
        result: dict = await client.load(KEY)
        assert result == data
        second_data = [4]
        await client.extend(KEY, second_data)
        result: dict = await client.load(KEY)
        assert result == [1, 2, 3, 4]
        await client.delete(KEY)


async def test_extract_method(redis_test_settings: RedisSettings):
    async for client in get_redis_connection(redis_test_settings):
        data = [1, 2, 3]
        await client.save(KEY, data)
        result: dict = await client.extract(KEY)
        assert result == data
        assert await client.load(KEY) == []


@pytest.mark.parametrize(
    'income_type',
    [
        list,
        tuple,
        dict,
        set,
        str,
    ],
)
async def test_load_empty(redis_test_settings: RedisSettings, income_type):
    async for client in get_redis_connection(redis_test_settings):
        result = await client.load(KEY, income_type)
        assert isinstance(result, income_type)
