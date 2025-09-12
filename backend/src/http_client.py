from aiohttp import ClientSession, ClientResponseError
import asyncio

class HTTPClient:
    """
    Базовый HTTP клиент для работы с API.
    Создает сессию aiohttp с заголовком API-ключа.
    """
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self._session = None  # Сессия создается лениво

    async def _get_session(self):
        # Если сессия не создана, создаем
        if self._session is None:
            self._session = ClientSession(
                base_url=self.base_url,
                headers={'X-CMC_PRO_API_KEY': self.api_key}
            )
        return self._session

    async def close(self):
        """
        Закрываем сессию aiohttp, чтобы избежать утечек ресурсов.
        Вызывать при shutdown приложения.
        """
        if self._session:
            await self._session.close()


class CMCHTTPClient(HTTPClient):
    """
    Клиент для работы с CoinMarketCap API.
    Реализует методы получения списка криптовалют и информации о конкретной валюте.
    """

    async def get_listings(self):
        """
        Получаем последние данные о криптовалютах.
        Endpoint: /v1/cryptocurrency/listings/latest
        """
        session = await self._get_session()
        async with session.get('/v1/cryptocurrency/listings/latest') as resp:
            resp.raise_for_status()  # Поднимет исключение, если ошибка HTTP
            data = await resp.json()
            return data.get('data', [])

    async def get_currency(self, currency_id: int):
        """
        Получаем подробную информацию о конкретной криптовалюте.
        Endpoint: /v1/cryptocurrency/quotes/latest
        """
        session = await self._get_session()
        async with session.get('/v1/cryptocurrency/quotes/latest', params={'id': currency_id}) as resp:
            resp.raise_for_status()
            data = await resp.json()
            # В API CoinMarketCap данные по ключу 'data' -> id валюты
            return data.get('data', {}).get(str(currency_id), {})
