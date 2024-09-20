from dataclasses import dataclass

import aiohttp
from aiohttp.client_exceptions import ClientError

from api.exeptions import DateValidationError


@dataclass
class Client:
    header = {"Content-Type": "application/json"}
    url: str
    data: dict | None = None

    async def post(self) -> dict:
        """Метод для добавления каких то данных."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
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
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
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
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.delete(
                    url=self.url,
                    headers=self.header
            ) as response:
                data: dict = await response.json()
                if response.status != 200:
                    message: str = data.get("detail").get("descr")
                    raise ClientError(message)

    async def patch(self) -> None:
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
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
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
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
