from src.redis_async_client import RedisSettings
from src.redis_async_client.core.maker import get_redis_connection


async def test_redis_health_check(redis_test_settings: RedisSettings):
    async for client in get_redis_connection(redis_test_settings):
        data = await client.health_check()
        assert data == {'test': 'test'}
