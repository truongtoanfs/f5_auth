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


apiConfig = ApiConfig()
