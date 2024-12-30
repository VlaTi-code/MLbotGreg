from dataclasses import dataclass

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from redis.asyncio import Redis
from aiogram import Router, F, BaseMiddleware
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from abc import ABC, abstractmethod
import time
from typing import Callable, Dict, Any, Union
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.filters import StateFilter

from states import UserState


class AntiSpamMiddleware(BaseMiddleware):
    """Middleware для обработки медиа-групп."""

    def __init__(self, latency: float = 0.5):
        """
        latency - время ожидания завершения группы.
        """
        super().__init__()
        self.album_data = {}
        self.latency = latency

    async def __call__(self, handler: Callable, event: Message, data: Dict[str, Any]):
        if not event.media_group_id:
            # Если сообщение не принадлежит группе, сразу передаём управление
            return await handler(event, data)

        media_group_id = event.media_group_id

        # Сохраняем сообщение в группе
        if media_group_id not in self.album_data:
            self.album_data[media_group_id] = []

        self.album_data[media_group_id].append(event)

        # Ожидаем завершения медиа-группы
        await asyncio.sleep(self.latency)

        # Если группа завершена, передаём весь альбом в хендлер
        if media_group_id in self.album_data:
            data["album"] = self.album_data.pop(media_group_id)
            return await handler(event, data)





@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class Config:
    tg_bot: TgBot
    database: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        database=DatabaseConfig(
            name=env('DB_NAME'),
            host=env('DB_HOST'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD'),
            port=env('DB_PORT'))
    )


config: Config = load_config('.env')

default = DefaultBotProperties(parse_mode='HTML')
bot: Bot = Bot(token=config.tg_bot.token, default=default)

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)
dp: Dispatcher = Dispatcher()

DATABASE_URL = (
    f"postgresql+asyncpg://{config.database.user}:{config.database.password}@"
    f"{config.database.host}/{config.database.name}"
)

BEER_PONG_EVENT_ID = 1
