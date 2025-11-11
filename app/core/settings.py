from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )

    # API Configuration
    API_V1: str
    PROJECT_NAME: str
    ENV: str = "development"

    # Database Configuration (Railway/Render provide DATABASE_URL directly)
    DATABASE_URL: str

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # Redis Configuration (Railway/Render provide REDIS_URL directly)
    REDIS_URL: str

    # Email Configuration
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    # Stripe Configuration
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str


def get_settings():
    return Settings()


settings = Settings()
