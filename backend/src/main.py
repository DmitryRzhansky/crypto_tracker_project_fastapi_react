from fastapi import FastAPI
from .http_client import CMCHTTPClient
from .config import settings
import asyncio

app = FastAPI(title="Crypto API", description="Пример FastAPI клиента для CoinMarketCap")

# Инициализация клиента с API ключом
cmc_client = CMCHTTPClient(
    base_url='https://pro-api.coinmarketcap.com',
    api_key=settings.CMC_API_KEY
)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Закрываем сессию aiohttp при завершении работы приложения
    """
    await cmc_client.close()


@app.get('/cryptocurrencies', summary="Список криптовалют")
async def get_cryptocurrencies():
    """
    Возвращает список всех криптовалют с последними данными.
    """
    return await cmc_client.get_listings()


@app.get('/cryptocurrencies/{currency_id}', summary="Информация о криптовалюте")
async def get_cryptocurrency(currency_id: int):
    """
    Возвращает подробную информацию о конкретной криптовалюте по ID.
    """
    return await cmc_client.get_currency(currency_id)
