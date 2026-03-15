import asyncio
import json
import logging
from contextlib import asynccontextmanager
from typing import Optional

import aiomqtt

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self, host: str, port: int, username: Optional[str], password: Optional[str], device_id: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.device_id = device_id
        self.last_status: Optional[str] = None
        self._listen_task: Optional[asyncio.Task] = None
        self._client: Optional[aiomqtt.Client] = None

    @asynccontextmanager
    async def _get_client(self):
        """Внутренний метод для создания клиента в контексте."""
        async with aiomqtt.Client(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        ) as client:
            yield client

    async def connect(self):
        """Подключение к брокеру и запуск прослушивания."""
        self._client = aiomqtt.Client(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        )
        await self._client.__aenter__()
        logger.info("MQTT connected to %s:%d", self.host, self.port)

        topic = f"esp/status/{self.device_id}"
        await self._client.subscribe(topic)
        logger.info("Subscribed to %s", topic)

        self._listen_task = asyncio.create_task(self._listen_loop())

    async def disconnect(self):
        """Отключение от брокера."""
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        if self._client:
            await self._client.__aexit__(None, None, None)
            logger.info("MQTT disconnected")

    async def _listen_loop(self):
        """Фоновая задача: читает входящие сообщения и обновляет last_status."""
        try:
            async for message in self._client.messages:
                payload = message.payload.decode()
                logger.debug("Received MQTT message on %s: %s", message.topic, payload)
                self.last_status = payload
        except asyncio.CancelledError:
            logger.info("MQTT listen task cancelled")
        except Exception as e:
            logger.exception("MQTT listen loop error: %s", e)

    async def publish_command(self, payload: dict):
        """Публикация команды в топик команд."""
        if not self._client:
            raise ConnectionError("MQTT client not connected")
        topic = f"esp/command/{self.device_id}"
        await self._client.publish(topic, payload=json.dumps(payload), qos=1)
        logger.info("Command published to %s: %s", topic, payload)