from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Message,
    CallbackQuery,
    ContentType,
)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder
)
from aiogram import Router, F, BaseMiddleware
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from core import bot
from database import db
from filters import IsNotDefault, IsChoosingModel, IsChoosingPlan, IsWaitingForPhotos
from keyboards import UserKeyboards
from lexicon import LEXICON, buttons, callbacks
from states import UserState
from bot import delete_message
from asyncio import Lock

router: Router = Router()
kb: UserKeyboards = UserKeyboards()

photo_lock = Lock()


async def user_check_limits(message: Message = None, callback: CallbackQuery = None) -> dict:
    value = message if message else callback

    user_id = await db.get_user_id_by_username(value.from_user.username)

    user_requests = await db.get_user_request_count(user_id)

    print(user_requests)

    interior_learning_requests = user_requests['interior']['learning']
    interior_generation_requests = user_requests['interior']['generation']

    dress_up_learning_requests = user_requests['dress_up']['learning']
    dress_up_generation_requests = user_requests['dress_up']['generation']

    user_limits = await db.get_user_plan_limits(user_id)

    interior_learning_limits = user_limits['interior']['learning']
    interior_generation_limits = user_limits['interior']['generation']

    dress_up_learning_limits = user_limits['dress_up']['learning']
    dress_up_generation_limits = user_limits['dress_up']['generation']

    return {
        "interior": {
            "learning": interior_learning_limits - interior_learning_requests,
            "generation": interior_generation_limits - interior_generation_requests,
        },
        "dress_up": {
            "learning": dress_up_learning_limits - dress_up_learning_requests,
            "generation": dress_up_generation_limits - dress_up_generation_requests,
        }
    }


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
    requests_left: dict = await user_check_limits(message=message)

    await message.answer(
        LEXICON['interior_regime_intro'].format(requests_left["interior"]["learning"],
                                                requests_left["interior"]["generation"]),
        reply_markup=kb.interior_regime()
    )


@router.callback_query(F.data == callbacks[buttons['interior_new_model']], IsNotDefault())
async def interior_new_model(callback: CallbackQuery, state: FSMContext):
    await delete_message(callback.message)

    requests_left: dict = await user_check_limits(callback=callback)

    if not requests_left["interior"]["learning"]:
        return await callback.message.answer(
            text="У вас закончились бесплатные обучения модели.\n"
                 "Пожалуйста, оформите подписку, если хотите получить больше возможностей.",
            reply_markup=kb.interior_upgrade_plan()
        )

    await callback.message.answer(
        LEXICON['interior_new_model_enter_model_name'],
        reply_markup=kb.creating_model()
    )
    await state.set_state(UserState.waiting_for_model_name)


@router.message(UserState.waiting_for_model_name)
async def interior_receive_model_name(message: Message, state: FSMContext):
    """
    Получаем от пользователя название новой модели и переключаемся в режим ожидания фотографий.
    Если пользователь внезапно нажал другую кнопку (другой режим), игнорируем, чтобы не сломать логику.
    """
    if message.text in (buttons['interior_regime'], buttons['dress_up_regime'], buttons['help']):
        return  # Игнорируем эти нажатия/ввод

    # Сбрасываем состояние и заново устанавливаем, чтобы не копить лишние данные
    await state.clear()
    await state.set_state(UserState.waiting_for_photos)

    # Сохраняем имя модели и пустой список фотографий
    await state.update_data(model_name=message.text, photos=[], already_warned=False)

    await message.answer(
        text=LEXICON['interior_new_model_enter_photos'].format((await state.get_data()).get("model_name")),
        reply_markup=kb.creating_model()
    )


@router.message(StateFilter(UserState.waiting_for_photos), F.photo)
async def interior_add_photo(message: Message, state: FSMContext):
    """
    Обработка входящих фотографий в режиме waiting_for_photos.
    Сохраняем file_id в FSMContext, чтобы потом использовать при обучении/сохранении модели.
    Благодаря 'async with photo_lock:' каждый входящий апдейт с фото
    будет обрабатываться строго по очереди, исключая «прыгающий» счётчик.
    """

    async with photo_lock:
        # Получаем текущее состояние (словарь).
        data = await state.get_data()
        # Достаём список уже добавленных фото (по умолчанию - пустой список).
        photos: List[str] = data.get("photos", [])

        # Берём file_id у последней (самой большой) фотографии
        file_id = message.photo[-1].file_id
        photos.append(file_id)

        # Обновляем состояние, сохранив новый список
        await state.update_data(photos=photos)

        count = len(photos)

        # Логика выбора клавиатуры / сообщений
        if count < 7:
            # Пока меньше 7 фото
            await message.answer(
                f"Добавлено {count} фотографий. Нужно минимум 7.",
                reply_markup=kb.creating_model()  # Кнопка "Назад в меню"
            )
        else:
            # Если >= 7 фото
            await message.answer(
                f"Добавлено {count} фотографий.",
                reply_markup=kb.stop_creating_model()  # Клавиатура с кнопкой "Создать модель" + "Назад"
            )


@router.callback_query(F.data == callbacks[buttons['interior_creating_model_continue']], IsWaitingForPhotos())
async def interior_stop_waiting_for_photos(callback: CallbackQuery, state: FSMContext):
    """
    Вызывается, когда пользователь нажимает "Создать модель" (если фото уже >=7).
    """
    data = await state.get_data()
    user_id = await db.get_user_id_by_username(callback.from_user.username)

    await db.add_model(
        user_id=user_id,
        model_name=data.get("model_name"),
        model_type="interior",
        files_id=",".join(data.get("photos", [])),
    )

    await db.add_request(
        user_id=user_id,
        model_type='interior',
        request_type='learning'
    )

    await state.clear()
    await state.set_state(UserState.default_state)

    # Сообщаем пользователю о старте обучения
    await callback.message.answer(
        f"Модель {data.get('model_name')} начала обучение с "
        f"{len(data.get('photos', []))} фотографиями.\n"
        f"Скоро она появится в списке ваших моделей."
    )


@router.callback_query(F.data == callbacks[buttons['interior_gen_with_existing_model']])
async def interior_gen_with_existing_model(callback: CallbackQuery, state: FSMContext):
    """
    Когда пользователь выбирает "Сгенерировать изображение с существующей моделью".
    """
    user_id = await db.get_user_id_by_username(callback.from_user.username)
    models_list = await db.get_models_by_user_id(user_id)

    requests_left: dict = await user_check_limits(callback=callback)

    if not requests_left["interior"]["generation"]:
        await state.set_state(UserState.choosing_plan)
        return await callback.message.answer(
            text="У вас закончились бесплатные генерации с помощью модели.\n"
                 "Пожалуйста, оформите подписку, если хотите получить больше возможностей.",
            reply_markup=kb.interior_upgrade_plan()
        )

    if not models_list:
        # Нет ни одной обученной модели
        await callback.message.answer("У вас ещё нет моделей", reply_markup=kb.start())
        return

    # Переключаемся в состояние выбора модели
    await state.set_state(UserState.choosing_model)

    await callback.message.answer(
        LEXICON['interior_gen_with_existing_model'],
        reply_markup=kb.choosing_model(models_list)
    )


@router.callback_query(lambda c: c.data and c.data.startswith("model_"), IsChoosingModel())
async def handle_model_selection(callback: CallbackQuery, state: FSMContext):
    model_name = callback.data.split("_", 1)[1]

    user_id = await db.get_user_id_by_username(callback.from_user.username)

    await db.add_request(
        user_id=user_id,
        model_type='interior',
        request_type='generation'
    )

    await state.set_state(UserState.default_state)
    return await callback.message.answer(f"Вы выбрали модель: {model_name}")


@router.callback_query(F.data == callbacks[buttons['interior_choose_plan']])
async def interior_choose_plan_handler(callback: CallbackQuery, state: FSMContext):
    """
        Выбор тарифа для Dress Up.
        """
    await state.set_state(UserState.choosing_plan)
    return await callback.message.answer(
        LEXICON['dress_up_choose_plan'],
        reply_markup=kb.interior_choose_plan()
    )

######################################## DRESS UP ########################################
@router.message(F.text == buttons['dress_up_regime'], IsNotDefault())
async def dress_up_regime_intro_handler(message: Message, state: FSMContext):
    requests_left = await user_check_limits(message=message)

    await state.set_state(UserState.default_state)
    return await message.answer(
        LEXICON['dress_up_regime_intro'].format(requests_left["dress_up"]["generation"]),
        reply_markup=kb.dress_up_regime()
    )


@router.callback_query(F.data == callbacks[buttons['dress_up_choose_plan']])
async def dress_up_choose_plan_handler(callback: CallbackQuery, state: FSMContext):
    """
    Выбор тарифа для Dress Up.
    """
    await state.set_state(UserState.choosing_plan)
    return await callback.message.answer(
        LEXICON['dress_up_choose_plan'],
        reply_markup=kb.dress_up_choose_plan()
    )
