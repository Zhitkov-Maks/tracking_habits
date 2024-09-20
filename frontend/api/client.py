from dataclasses import dataclass

import aiohttp
from aiohttp.client_exceptions import ClientError

from api.exeptions import DateValidationError
from http import HTTPStatus as status


@dataclass
class Client:
    """
    Клиент для работы с tracking api. Нужен, чтобы убрать повторяющийся код.
    """
    url: str
    data: dict | None = None
    header = {"Content-Type": "application/json"}

    async def post(self) -> dict:
        """Метод для POST запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.post(
                url=self.url,
                json=self.data,
                headers=self.header
            ) as response:

                data: dict = await response.json()

                if (response.status == status.CREATED or
                    response.status == status.OK):
                    return data

                elif response.status == status.BAD_REQUEST:
                    message: str = data.get("detail").get("descr")
                    raise DateValidationError(message)

                else:
                    message: str = data.get("detail").get("descr")
                    raise ClientError(message)

    async def get(self) -> dict:
        """Метод для GET запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.get(
                    url=self.url,
                    headers=self.header
            ) as response:

                data: dict = await response.json()

                if response.status == status.OK:
                    return data

                else:
                    message: str = data.get("detail").get("descr")
                    raise ClientError(message)

    async def delete(self) -> None:
        """Метод для DELETE запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.delete(
                    url=self.url,
                    headers=self.header
            ) as response:

                data: dict = await response.json()

                if response.status != status.OK:
                    message: str = data.get("detail").get("descr")
                    raise ClientError(message)

    async def patch(self) -> None:
        """Метод для PATCH запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.patch(
                    url=self.url,
                    json=self.data,
                    headers=self.header
            ) as response:

                data: dict = await response.json()

                if response.status != status.OK:
                    message: str = data.get("detail").get("descr")
                    raise ClientError(message)

    async def put(self) -> dict:
        """Метод для PUT запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.put(
                url=self.url,
                json=self.data,
                headers=self.header
            ) as response:

                data: dict = await response.json()

                if response.status == status.OK:
                    return data

                else:
                    message: str = data.get("detail").get("descr")
                    raise ClientError(message)
