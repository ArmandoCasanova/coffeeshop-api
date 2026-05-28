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

    # OAuth Configuration - Google
    GOOGLE_OAUTH_CLIENT_ID: str = ""
    GOOGLE_OAUTH_CLIENT_SECRET: str = ""
    GOOGLE_OAUTH_REDIRECT_URI: str = ""

    # OAuth Configuration - GitHub
    GITHUB_OAUTH_CLIENT_ID: str = ""
    GITHUB_OAUTH_CLIENT_SECRET: str = ""
    GITHUB_OAUTH_REDIRECT_URI: str = ""

    # Session Configuration
    SESSION_TIMEOUT: int = 86400  # 24 horas en segundos

    # E2E Testing Configuration
    E2E_TEST_EMAIL: str = ""
    E2E_TEST_VERIFICATION_CODE: str = "0000"

    # Rate limiting 
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW_SECONDS: int = 60



def get_settings():
    return Settings()


settings = Settings()
