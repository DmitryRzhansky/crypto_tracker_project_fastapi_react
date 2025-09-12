from fastapi import FastAPI
from .router import router as router_crypto

app = FastAPI(title="Crypto API", description="Пример FastAPI клиента для CoinMarketCap")

# Подключаем роутер с маршрутами
app.include_router(router_crypto)
