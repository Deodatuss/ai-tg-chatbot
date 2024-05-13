from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr

    model_config = SettingsConfigDict(
        env_file="/thesis/.env",
        env_file_encoding="utf-8",
    )


config = Settings()
