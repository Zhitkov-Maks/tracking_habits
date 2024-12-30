from dataclasses import dataclass
from typing import Tuple, Dict, List

import aiohttp


@dataclass
class Client:
    """
    A class for server requests, implemented to reduce the amount
    of repetitive code.
    """
    url: str
    data: dict | None = None
    header = {"Content-Type": "application/json"}

    async def post(self) -> Tuple[int, dict]:
        """A method for implementing post requests."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)) as client:
            async with client.post(
                    url=self.url, json=self.data, headers=self.header
            ) as response:
                data: dict = await response.json()
                return response.status, data

    async def get(self) -> Tuple[int, Dict[str, List[Dict[str, int]] | Dict[str, str]]]:
        """A method for implementing get requests."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.get(
                    url=self.url,
                    headers=self.header
            ) as response:

                data: Dict[str, List[Dict[str, int]] | Dict[str, str]] = await response.json()
                return response.status, data

    async def delete(self) -> Tuple[int, dict]:
        """A method for implementing delete requests."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.delete(
                    url=self.url, headers=self.header) as response:
                data: dict = await response.json()
                return response.status, data

    async def patch(self) -> Tuple[int, dict]:
        """A method for implementing patch requests."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.patch(
                    url=self.url, json=self.data, headers=self.header
            ) as response:
                data: dict = await response.json()
                return response.status, data

    async def put(self) -> Tuple[int, dict]:
        """A method for implementing put requests."""
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(60)
        ) as client:
            async with client.put(
                url=self.url, json=self.data, headers=self.header
            ) as response:
                data: dict = await response.json()
                return response.status, data
