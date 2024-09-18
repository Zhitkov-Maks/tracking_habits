import aiohttp
from aiohttp.client_exceptions import ClientError

from api.exeptions import DateValidationError


class Client:

    def __init__(self, url: str, data: dict | None = None):
        self.data = data
        self.url = url
        self.header = {"Content-Type": "application/json"}

    @classmethod
    async def _client(cls):
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            return client

    async def post(self) -> dict:
        """Метод для добавления каких то данных."""
        client = await self._client()
        async with client.post(
            url=self.url,
            json=self.data,
            headers=self.header
    ) as response:
            data: dict = await response.json()
            if response.status == 201 or response.status == 200:
                return data

            elif response.status == 400:
                message: str = data.get("detail").get("descr")
                raise DateValidationError(message)

            else:
                message: str = data.get("detail").get("descr")
                raise ClientError(message)

    async def get(self) -> dict:
        """Метод для получения каких то данных."""
        client = await self._client()
        async with client.get(
                url=self.url,
                headers=self.header
        ) as response:
            data: dict = await response.json()
            if response.status == 200:
                return data

            else:
                message: str = data.get("detail").get("descr")
                raise ClientError(message)

    async def delete(self) -> None:
        client = await self._client()
        async with client.delete(
                url=self.url,
                headers=self.header
        ) as response:
            data: dict = await response.json()
            if response.status != 200:
                message: str = data.get("detail").get("descr")
                raise ClientError(message)

    async def patch(self) -> None:
        client = await self._client()
        async with client.patch(
                url=self.url,
                json=self.data,
                headers=self.header
        ) as response:
            data: dict = await response.json()
            if response.status != 200:
                message: str = data.get("detail").get("descr")
                raise ClientError(message)

    async def put(self) -> dict:
        """Метод для добавления каких то данных."""
        client = await self._client()
        async with client.put(
            url=self.url,
            json=self.data,
            headers=self.header
        ) as response:
            data: dict = await response.json()

            if response.status == 200:
                return data
            else:
                message: str = data.get("detail").get("descr")
                raise ClientError(message)
