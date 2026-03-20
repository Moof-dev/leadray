from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    #db settings
    DB_HOSTNAME: str = "db"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "database_name"

    #redis settings
    CACHE_HOSTNAME: str = "cache"
    CACHE_DB: int = 0

    #jwt
    JWT_SECRET_KEY: str = "secret"
    JWT_ENCODE_ALGORITHM: str = "HS256"

    #celery
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq//"


    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}/{self.DB_NAME}"

    @property
    def redis_url(self) -> str:
        return f"redis://{self.CACHE_HOSTNAME}/{self.CACHE_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()