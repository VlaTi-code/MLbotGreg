from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from core import config
from database import db
from states import UserState


# class IsAdmin(Filter):
#     async def __call__(self, message: Message, *args, **kwargs):
#         return message.from_user.id in config.tg_bot.admin_ids or message.from_user.id in config.tg_bot.admin_ids


class IsNotDefault(Filter):
    async def __call__(self, message: Message, state: FSMContext, *args, **kwargs):
        state_value = await state.get_state()
        return state_value in [None, default_state]

class IsChoosingModel(Filter):
    async def __call__(self, message: Message, state: FSMContext, *args, **kwargs):
        state_value = await state.get_state()
        return state_value == UserState.choosing_model

class IsChoosingPlan(Filter):
    async def __call__(self, message: Message, state: FSMContext, *args, **kwargs):
        state_value = await state.get_state()
        return state_value == UserState.choosing_plan

class IsWaitingForPhotos(Filter):
    async def __call__(self, message: Message, state: FSMContext, *args, **kwargs):
        state_value = await state.get_state()
        return state_value == UserState.waiting_for_photos
