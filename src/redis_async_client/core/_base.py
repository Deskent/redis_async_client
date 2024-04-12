import json
from abc import abstractmethod

from redis.asyncio import Redis

from ._constants import STORE_TIME_SEC
from ._logger import logger
from ._types import JSON
from .exc import RedisAsyncClientException


class RedisBase:
    """Store data in redis.

    Attributes:

        client: Redis - Redis db connect instance

    """

    def __init__(self, client: Redis):
        self.client: Redis = client


class BaseOperator(RedisBase):
    def __init__(self, client: Redis, key: str):
        super().__init__(client)
        self.key: str = key

    async def run(self) -> JSON | None:
        try:
            return await self._execute()
        except ConnectionRefusedError as err:
            error_text: str = (
                f'\nUnable to connect to redis, data: not saved!\n{err}'
            )
        except ConnectionError as err:
            error_text = f'Connection error: {err}'
        except Exception as err:
            logger.exception(err)
            error_text = f'Exception error: {err}'
        logger.error(error_text)
        raise RedisAsyncClientException(error_text)

    @abstractmethod
    async def _execute(self, *args, **kwargs):
        raise NotImplementedError


class SaveOperator(BaseOperator):
    """Save data to Redis by key."""

    def __init__(
        self,
        data: JSON,
        timeout_sec: int = STORE_TIME_SEC,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.timeout_sec: int = timeout_sec
        self._data: JSON = data

    async def _execute(self) -> None:
        """Save serialized data to redis by key using timeout."""

        value: str = json.dumps(self._data, default=str)
        return await self.client.set(
            name=self.key,
            value=value,
            ex=self.timeout_sec,
        )


class LoadOperator(BaseOperator):
    """Load data from Redis by key"""

    async def _execute(self) -> JSON:
        """Load data from redis. Return deserialized."""

        data: str = await self.client.get(self.key)
        if not data:
            return []
        return json.loads(data)


class DeleteOperator(BaseOperator):
    """Delete data from Redis by key"""

    async def _execute(self) -> None:
        """Delete data from Redis by key"""

        await self.client.delete(self.key)


class UpdateOperator(SaveOperator):
    """Update dictionary data by key"""

    async def _execute(self) -> dict:
        """Update dictionary data by key"""

        old_data: str = await self.client.get(self.key)
        if not old_data:
            old_data: dict = {}
        else:
            old_data: dict = json.loads(old_data)
        for elem in (old_data, self._data):
            if not isinstance(elem, dict):
                raise RedisAsyncClientException(
                    f'Data for update must be dictionary, got {type(elem)}'
                )

        old_data.update(self._data)
        new_data: str = json.dumps(old_data)
        await self.client.set(
            name=self.key,
            value=new_data,
            ex=self.timeout_sec,
        )

        return old_data


class AppendOperator(SaveOperator):
    """Append data to list"""

    async def _execute(self) -> list:
        """Append data to list"""

        old_data: str = await self.client.get(self.key)
        if not old_data:
            old_data: list = []
        else:
            old_data: list = json.loads(old_data)
        if not isinstance(old_data, list):
            raise RedisAsyncClientException(
                f'Existing data must be list, got {type(old_data)}'
            )

        old_data.append(self._data)
        new_data: str = json.dumps(old_data)
        await self.client.set(
            name=self.key,
            value=new_data,
            ex=self.timeout_sec,
        )

        return old_data


class ExtendOperator(SaveOperator):
    """Extend list with data."""

    async def _execute(self) -> list:
        """Append data to list"""

        if not isinstance(self._data, list):
            raise RedisAsyncClientException(
                f'Data must be list, got {type(self._data)}'
            )

        old_data: str = await self.client.get(self.key)
        if not old_data:
            old_data: list = []
        else:
            old_data: list = json.loads(old_data)
        if not isinstance(old_data, list):
            raise RedisAsyncClientException(
                f'Existing data must be list, got {type(old_data)}'
            )

        old_data.extend(self._data)
        new_data: str = json.dumps(old_data)
        await self.client.set(
            name=self.key,
            value=new_data,
            ex=self.timeout_sec,
        )

        return old_data
