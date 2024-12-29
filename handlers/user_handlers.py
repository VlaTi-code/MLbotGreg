from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext

from core import bot
# from database import db
from filters import IsNotCreatingModel
from keyboards import UserKeyboards
from lexicon import LEXICON, buttons, callbacks

from states import UserState

# from utils import validate_and_format_phone_number, convert_string_to_date, validate_date_of_birth


router: Router = Router()
kb: UserKeyboards = UserKeyboards()


#########################################################################################
######################################## GENERAL ########################################
#########################################################################################
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(UserState.default_state)

    # if not await db.user_exists(message.from_user.id):
    #     await db.init_user(message.from_user.id, message.from_user.username)

    await message.answer(LEXICON['start'], reply_markup=kb.start())
    await state.set_state(UserState.default_state)


@router.message(F.text == buttons['help'])
async def help_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON['help'], reply_markup=kb.start())


@router.callback_query(F.data == callbacks[buttons['back_to_menu']])
async def back_to_menu_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON['start'], reply_markup=kb.start())


#########################################################################################
######################################## REGIMES ########################################
#########################################################################################

######################################## INTERIOR ########################################
@router.message(F.text == buttons['interior_regime'], IsNotCreatingModel())
async def interior_regime_intro_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON['interior_regime_intro'], reply_markup=kb.interior_regime())


@router.callback_query(F.data == callbacks[buttons['interior_new_model']], IsNotCreatingModel())
async def interior_new_model(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON['interior_new_model_enter_model_name'])
    await state.set_state(UserState.waiting_for_model_name)


@router.message(UserState.waiting_for_model_name)
async def interior_receive_model_name(message: Message, state: FSMContext):
    await state.update_data(model_name=message.text)
    await state.set_state(UserState.waiting_for_photos)
    await message.answer(text=LEXICON['interior_new_model_enter_photos'])


@router.message(UserState.waiting_for_photos, F.content_type == ContentType.PHOTO)
async def interior_receive_photos(message: Message, state: FSMContext):
    if len(message.photo) < 7:
        await message.answer(text=LEXICON['interior_new_model_enter_photos_failed_not_enough_photos'])
    elif len(message.photo) > 10:
        await message.answer(text=LEXICON['interior_new_model_enter_photos_failed_not_enough_photos'])
    else:
        model_name = (await state.get_data()).get("model_name")
        await state.clear()
        await message.answer(f"Модель '{model_name}' успешно создана!")
        await state.set_state(UserState.default_state)


######################################## DRESS UP ########################################
@router.message(F.text == buttons['dress_up_regime'])
async def dress_up_regime_intro_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON['dress_up_regime_intro'], reply_markup=kb.dress_up_regime())
