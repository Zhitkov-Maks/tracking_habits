from dataclasses import dataclass
from typing import Tuple

import aiohttp


@dataclass
class Client:
    """
    Клиент для работы с tracking api. Нужен, чтобы убрать повторяющийся код.
    """
    url: str
    data: dict | None = None
    header = {"Content-Type": "application/json"}

    async def post(self) -> Tuple[int, dict]:
        """Метод для POST запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)) as client:
            async with client.post(
                    url=self.url, json=self.data, headers=self.header
            ) as response:
                data: dict = await response.json()
                return response.status, data

    async def get(self) -> Tuple[int, dict]:
        """Метод для GET запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.get(
                    url=self.url,
                    headers=self.header
            ) as response:

                data: dict = await response.json()
                return response.status, data

    async def delete(self) -> Tuple[int, dict]:
        """Метод для DELETE запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.delete(
                    url=self.url, headers=self.header) as response:
                data: dict = await response.json()
                return response.status, data

    async def patch(self) -> Tuple[int, dict]:
        """Метод для PATCH запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.patch(
                    url=self.url, json=self.data, headers=self.header
            ) as response:
                data: dict = await response.json()
                return response.status, data

    async def put(self) -> Tuple[int, dict]:
        """Метод для PUT запросов."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.put(
                url=self.url, json=self.data, headers=self.header
            ) as response:
                data: dict = await response.json()
                return response.status, data
