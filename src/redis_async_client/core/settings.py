import dataclasses

import redis


@dataclasses.dataclass
class RedisSettings:
    """Redis settings dataclass.

    Attributes:

        REDIS_HOST: str = '127.0.0.1'

        REDIS_PORT: int = 6379

        REDIS_DB: int = 0

    Methods
        get_url

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

    def make_pool(self, url: str = '') -> redis.asyncio.ConnectionPool:
        if not url:
            url = self.get_url()
        return redis.asyncio.ConnectionPool.from_url(url)
