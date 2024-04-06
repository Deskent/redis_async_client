from ._constants import STORE_TIME_SEC
from ._types import JSON
from .base import (
    AppendRedisDB,
    DeleteRedisDB,
    GetRedisDB,
    RedisBase,
    SetRedisDB,
    UpdateRedisDB,
)
from .logger import logger


class AsyncRedisClient(RedisBase):
    """
    Class for work with Redis database

        Methods:
            save() - Save data to Redis database.

            load() - Load data from Redis database.

            delete() - Delete data from Redis database.

            update() - Update dictionary into Redis database.

            append() - Append list into Redis database.

            extract() - Load data and delete key from Redis database.

            health_check() - Save, load and delete test key in Redis database.
    """

    async def health_check(self):
        """Check redis work."""

        key: str = 'redis_auto_test'
        logger.info('Redis checking...')
        test_data: dict = {'test': 'test'}
        await self.save(key, test_data, 60)
        results: dict = await self.load(key)
        logger.info('Redis checking: OK')
        await self.delete(key)

        return results

    async def save(
        self,
        key: str,
        data: JSON,
        timeout_sec: int = STORE_TIME_SEC,
    ) -> JSON:
        logger.debug(
            f'Key [{key}]: Timeout: {timeout_sec}. Saved data: {len(data)}'
        )

        return await SetRedisDB(
            client=self.client,
            key=key,
            data=data,
            timeout_sec=timeout_sec,
        ).run()

    async def load(self, key: str) -> JSON:
        """Load key from redis."""

        data: JSON = await GetRedisDB(
            client=self.client,
            key=key,
        ).run()
        logger.debug(f'Key [{key}]: load data: {len(data)}')

        return data

    async def delete(self, key: str) -> None:
        """Delete key from redis."""

        logger.debug(f'Key [{key}]: deleted')

        return await DeleteRedisDB(
            client=self.client,
            key=key,
        ).run()

    async def update(
        self,
        key: str,
        data: JSON,
        timeout_sec: int = STORE_TIME_SEC,
    ) -> dict:
        """Update dictionary data."""

        logger.debug(
            f'Key [{key}]: Timeout: {timeout_sec}. '
            f'Data will be update: {len(data)}'
        )

        updated: dict = await UpdateRedisDB(
            client=self.client,
            key=key,
            data=data,
            timeout_sec=timeout_sec,
        ).run()

        return updated

    async def append(
        self,
        key: str,
        data: JSON,
        timeout_sec: int = STORE_TIME_SEC,
    ) -> list:
        """Append data to list."""

        appended: list = await AppendRedisDB(
            client=self.client,
            key=key,
            data=data,
            timeout_sec=timeout_sec,
        ).run()

        logger.debug(
            f'Key [{key}]: Timeout: {timeout_sec}. '
            f'Data appended. Now: {len(appended)}'
        )

        return appended

    async def extract(self, key: str) -> JSON:
        """Load data from Redis and delete its key."""

        data: JSON = await self.load(key)
        await self.delete(key)

        return data
