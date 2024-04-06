import dataclasses

import redis.asyncio as redis


@dataclasses.dataclass
class RedisSettings:
    """Redis settings class.

    Attributes:

        REDIS_HOST: str = '127.0.0.1'

        REDIS_PORT: int = 6379

        REDIS_DB: int = 0

    Methods
        get_url_by_name

        make_pool

    """

    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    def get_url(self) -> str:
        """Returns full Redis url."""

        redis_url: str = (
            f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'
        )

        return redis_url

    def make_pool(self, url: str = '') -> redis.ConnectionPool:
        if not url:
            url = self.get_url()
        return redis.ConnectionPool.from_url(url)


redis_settings = RedisSettings()
