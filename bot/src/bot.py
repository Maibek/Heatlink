import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.src.config import config
from bot.src.mqtt_client import MQTTClient

# Важно для Windows: используем SelectorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

# Хендлеры
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!\n"
                         "Доступные команды:\n"
                         "/status - текущий статус устройства\n"
                         "/set_temp <градусы> - установить температуру")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    # Получаем клиента из bot
    mqtt = message.bot.mqtt_client if hasattr(message.bot, 'mqtt_client') else None
    if not mqtt or not hasattr(mqtt, '_client') or mqtt._client is None:
        await message.answer("Нет подключения к устройству.")
        return
    if mqtt.last_status:
        await message.answer(f"Последний статус:\n{mqtt.last_status}")
    else:
        await message.answer("Статус ещё не получен.")

@dp.message(Command("set_temp"))
async def cmd_set_temp(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Использование: /set_temp <значение>")
        return
    try:
        temp = float(args[1])
    except ValueError:
        await message.answer("Значение должно быть числом.")
        return

    mqtt = message.bot.mqtt_client if hasattr(message.bot, 'mqtt_client') else None
    if not mqtt or not hasattr(mqtt, '_client') or mqtt._client is None:
        await message.answer("Нет подключения к устройству.")
        return

    # Формируем команду
    command = {"action": "set_temp", "value": temp}
    try:
        await mqtt.publish_command(command)
        await message.answer(f"Команда на установку температуры {temp}°C отправлена.")
    except Exception as e:
        logger.exception("Ошибка при отправке команды")
        await message.answer("Ошибка при отправке команды.")

# Запуск
async def main():
    # Создаём MQTT клиент
    mqtt_client = MQTTClient(
        host=config.mqtt_host,
        port=config.mqtt_port,
        username=config.mqtt_user,
        password=config.mqtt_password.get_secret_value() if config.mqtt_password else None,
        device_id=config.device_id
    )
    await mqtt_client.connect()
    # Сохраняем клиента как атрибут бота
    bot.mqtt_client = mqtt_client

    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await mqtt_client.disconnect()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())