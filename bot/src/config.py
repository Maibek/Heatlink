import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

# Определяем путь к .env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8', extra='ignore')

    # Telegram Bot
    bot_token: SecretStr = Field(..., validation_alias='BOT_TOKEN')

    # MQTT Broker
    mqtt_host: str = Field(..., validation_alias='MQTT_HOST')
    mqtt_port: int = Field(1883, validation_alias='MQTT_PORT')
    mqtt_user: str | None = Field(None, validation_alias='MQTT_USER')
    mqtt_password: SecretStr | None = Field(None, validation_alias='MQTT_PASSWORD')

    # Device
    device_id: str = Field(..., validation_alias='DEVICE_ID')

config = Config()