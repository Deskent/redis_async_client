### Installation

    pip install redis-async-client

### Usage Async

    from redis_async_client import AsyncRedisClient, RedisSettings

    redis_settings = RedisSettings()
    pool: redis_async.ConnectionPool = redis_settings.make_pool()
    async with redis_async.Redis(connection_pool=pool) as conn:
        async_client = AsyncRedisClient(conn)
        data = await async_client.health_check()
        assert data == {'test': 'test'}

    or

    from redis_async_client import RedisSettings, get_redis_connection

    redis_settings = RedisSettings()
    async for client in get_redis_connection(redis_settings):
        data = await client.health_check()
        assert data == {'test': 'test'}
