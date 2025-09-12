from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ключ API для CoinMarketCap. Берется из файла .env
    CMC_API_KEY: str

    # Конфигурация Pydantic: загружаем переменные окружения из .env
    model_config = SettingsConfigDict(env_file='.env')


# Создаем глобальный объект настроек, чтобы использовать везде
settings = Settings()
