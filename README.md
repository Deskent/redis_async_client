### Stack:

- [x] <a href="https://www.python.org/"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-plain.svg" alt="python" width="15" height="15"/>
  Python 3.10+ <br/></a>
- [x] <a href="https://github.com/redis/redis-py"><img src="https://avatars.githubusercontent.com/u/1529926?s=48&v=4" alt="niquests" width="15" height="15"/>
  Redis 5.0.3+ <br/>

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
