import aiohttp
from aiohttp.client_exceptions import ClientError


class Client:

    def __init__(self, url: str, data: dict):
        self.data = data
        self.url = url
        self.header = {"Content-Type": "application/json"}

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

                if response.status == 201:
                    return data

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
