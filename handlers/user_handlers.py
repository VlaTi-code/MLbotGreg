from time import time

from abc import ABC

from aiogram import Router, F, BaseMiddleware
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from core import bot, AntiSpamMiddleware
from database import db
from filters import IsNotDefault, IsChoosingModel, IsChoosingPlan
from keyboards import UserKeyboards
from lexicon import LEXICON, buttons, callbacks
from states import UserState
from bot import delete_message
from aiogram.filters import StateFilter

from typing import List

router: Router = Router()
kb: UserKeyboards = UserKeyboards()

router.message.middleware(AntiSpamMiddleware())


#########################################################################################
######################################## GENERAL ########################################
#########################################################################################
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(UserState.default_state)
    await db.add_user(message.from_user.username)
    await message.answer(LEXICON['start'], reply_markup=kb.start())
    return await state.set_state(UserState.default_state)


@router.message(F.text == buttons['help'])
async def help_handler(message: Message, state: FSMContext):
    return await message.answer(LEXICON['help'], reply_markup=kb.start())


@router.callback_query(F.data == callbacks[buttons['back_to_menu']])
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(UserState.default_state)
    return await callback.message.answer(LEXICON['start'], reply_markup=kb.start())


#########################################################################################
######################################## REGIMES ########################################
#########################################################################################

######################################## INTERIOR ########################################
@router.message(F.text == buttons['interior_regime'], IsNotDefault())
async def interior_regime_intro_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON['interior_regime_intro'], reply_markup=kb.interior_regime())


@router.callback_query(F.data == callbacks[buttons['interior_new_model']], IsNotDefault())
async def interior_new_model(callback: CallbackQuery, state: FSMContext):
    await delete_message(callback.message)
    await callback.message.answer(LEXICON['interior_new_model_enter_model_name'],
                                  reply_markup=kb.creating_model())
    await state.set_state(UserState.waiting_for_model_name)


@router.message(UserState.waiting_for_model_name)
async def interior_receive_model_name(message: Message, state: FSMContext):
    # Сбрасываем всё и переводим в ожидание фотографий
    if message.text == buttons['interior_regime'] or \
            message.text == buttons['dress_up_regime'] or \
            message.text == buttons['help']:
        return

    await state.clear()
    await state.set_state(UserState.waiting_for_photos)
    await state.update_data(model_name=message.text, photos=[], already_warned=False)
    await message.answer(
        text=LEXICON['interior_new_model_enter_photos'].format((await state.get_data()).get("model_name")),
        reply_markup=kb.creating_model())


@router.message(StateFilter(UserState.waiting_for_photos))
async def handle_album(message: Message, state: FSMContext, album: List[Message] = None):
    """Обработка медиа-групп."""

    if not album or len(album) < 7:
        await message.answer("Фотографий недостаточно. Нужно отправить от 7 до 10 фотографий.")
        return

    if len(album) > 10:
        await message.answer("Слишком много фотографий. Отправьте от 7 до 10.")
        return

    # Обработка корректного альбома
    media_group = [obj.photo[-1].file_id for obj in album if obj.photo]

    # Сохраняем модель
    data = await state.get_data()
    user_id = await db.get_user_id_by_username(message.from_user.username)
    await db.add_model(
        user_id=user_id,
        model_name=data.get("model_name"),
        model_type="interior",
        files_id=",".join(media_group)
    )

    await message.answer(f"Модель успешно создана с {len(media_group)} фотографиями!")
    await state.clear()
    await state.set_state(UserState.default_state)


@router.callback_query(F.data == callbacks[buttons['interior_gen_with_existing_model']])
async def interior_gen_with_existing_model(callback: CallbackQuery, state: FSMContext):
    print("dgjkbnsadfkhfgnafsdkjgf")
    user_id = await db.get_user_id_by_username(callback.from_user.username)
    models_list = await db.get_models_by_user_id(user_id)
    print(models_list)
    print(user_id)

    if not models_list:
        await callback.message.answer("У вас ещё нет моделей", reply_markup=kb.start())
        return

    await state.set_state(UserState.choosing_model)
    return await callback.message.answer(LEXICON['interior_gen_with_existing_model'],
                                reply_markup=kb.choosing_model(models_list))


@router.callback_query(lambda c: c.data and c.data.startswith("model_"), IsChoosingModel())
async def handle_model_selection(callback: CallbackQuery, state: FSMContext):
    model_name = callback.data.split("_", 1)[1]

    await state.set_state(UserState.default_state)
    return await callback.message.answer(f"Вы выбрали модель: {model_name}")


# @router.callback_query()
# async def log_callback_data(callback: CallbackQuery):
#     print(f"Callback data: {callback.data}")
#     await callback.answer()

######################################## DRESS UP ########################################
@router.message(F.text == buttons['dress_up_regime'], IsNotDefault())
async def dress_up_regime_intro_handler(message: Message, state: FSMContext):
    await state.set_state(UserState.default_state)
    return await message.answer(LEXICON['dress_up_regime_intro'],
                                reply_markup=kb.dress_up_regime())


@router.callback_query(F.data == callbacks[buttons['dress_up_choose_plan']])
async def dress_up_choose_plan_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.choosing_plan)
    return await callback.message.answer(LEXICON['dress_up_choose_plan'],
                                reply_markup=kb.dress_up_choose_plan())


# @router.callback_query

