from fastapi import APIRouter
from .http_client import CMCHTTPClient
from .config import settings

# Инициализация клиента CoinMarketCap
cmc_client = CMCHTTPClient(
    base_url='https://pro-api.coinmarketcap.com',
    api_key=settings.CMC_API_KEY
)

# Создаем отдельный роутер с префиксом /currencies
router = APIRouter(
    prefix='/currencies',
    tags=['cryptocurrencies']  # теги для документации Swagger
)

@router.get('/', summary="Список криптовалют")
async def get_cryptocurrencies():
    """
    Возвращает список всех криптовалют с последними данными.
    """
    return await cmc_client.get_listings()


@router.get('/{currency_id}', summary="Информация о криптовалюте")
async def get_cryptocurrency(currency_id: int):
    """
    Возвращает подробную информацию о конкретной криптовалюте по ID.
    """
    return await cmc_client.get_currency(currency_id)
