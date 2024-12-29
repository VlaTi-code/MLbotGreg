from typing import List

from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils import keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from lexicon import buttons, callbacks


class UserKeyboards:
    @staticmethod
    def start() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=buttons['interior_regime']), KeyboardButton(text=buttons['dress_up_regime'])],
                [KeyboardButton(text=buttons['help'])]
            ]
        )

        return kb

    @staticmethod
    def interior_regime() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['interior_new_model'],
                                      callback_data=callbacks[buttons['interior_new_model']])],
                [InlineKeyboardButton(text=buttons['interior_gen_with_existing_model'],
                                      callback_data=callbacks[buttons['interior_gen_with_existing_model']])],
                [InlineKeyboardButton(text=buttons['interior_choose_plan'],
                                      callback_data=callbacks[buttons['interior_choose_plan']])],
                [InlineKeyboardButton(text=buttons['back_to_menu'],
                                      callback_data=callbacks[buttons['back_to_menu']])]
            ]
        )

        return kb

    @staticmethod
    def dress_up_regime() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['dress_up_new_gen'],
                                      callback_data=callbacks[buttons['dress_up_new_gen']])],
                [InlineKeyboardButton(text=buttons['dress_up_choose_plan'],
                                      callback_data=callbacks[buttons['dress_up_choose_plan']])],
                [InlineKeyboardButton(text=buttons['back_to_menu'],
                                      callback_data=callbacks[buttons['back_to_menu']])]
            ]
        )

        return kb
