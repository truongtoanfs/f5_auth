from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    TITLE: str = "Auth Service"
    DOC_URL: str = "/api/v1/dashboard/docs"
    VERSION: str = "1.0.0"
    CONTACT: dict = {
        "name": "toanfs",
        "email": "toan.truongvanfs@gmail.com",
    }

    PASSWORD_EXPIRED: int = 2 * 24 * 60 * 60
    MYSQL_URL: str
    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str
    TOKEN_SECRET_KEY: str
    # Redis Config
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str
    # Captcha Config
    CAPTCHA_ENABLE: bool = True
    CAPTCHA_URL: str = "https://www.google.com/recaptcha/api/siteverify"
    CAPTCHA_SECRET: str


apiConfig = ApiConfig()
