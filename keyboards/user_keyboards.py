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
    def interior_choose_plan() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['interior_standard'],
                                      callback_data=callbacks[buttons['interior_standard']])],
                [InlineKeyboardButton(text=buttons['interior_pro'],
                                      callback_data=callbacks[buttons['interior_pro']])],
                [InlineKeyboardButton(text=buttons['interior_premium'],
                                      callback_data=callbacks[buttons['interior_premium']])],
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

    @staticmethod
    def dress_up_choose_plan() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['dress_up_standard'],
                                      callback_data=callbacks[buttons['dress_up_standard']])],
                [InlineKeyboardButton(text=buttons['dress_up_pro'],
                                      callback_data=callbacks[buttons['dress_up_pro']])],
                [InlineKeyboardButton(text=buttons['dress_up_premium'],
                                      callback_data=callbacks[buttons['dress_up_premium']])],
                [InlineKeyboardButton(text=buttons['back_to_menu'],
                                      callback_data=callbacks[buttons['back_to_menu']])]
            ]
        )

        return kb

    @staticmethod
    def creating_model() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['back_to_menu'],
                                      callback_data=callbacks[buttons['back_to_menu']])],
            ]
        )

        return kb

    @staticmethod
    def stop_creating_model():
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=buttons['interior_creating_model_continue'],
                        callback_data=callbacks[buttons['interior_creating_model_continue']]
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=buttons['back_to_menu'],
                        callback_data=callbacks[buttons['back_to_menu']]
                    )
                ],
            ]
        )
        return kb

    @staticmethod
    def choosing_model(models_list) -> InlineKeyboardMarkup:
        inline_keyboard = []
        for model in models_list:
            # Превращаем модель в строку, если это вдруг не строка
            model_str = str(model)
            # Ограничиваем длину, чтобы не вылететь за 64 байта
            callback_data_value = f"model_{model_str[:20]}"  # 20 символов + 'model_'
            print(callback_data_value)
            inline_keyboard.append([
                InlineKeyboardButton(
                    text=model_str,
                    callback_data=callback_data_value
                )
            ])
        # Исправление структуры для "Назад в меню"
        inline_keyboard.append([
            InlineKeyboardButton(
                text=buttons['back_to_menu'],
                callback_data=callbacks[buttons['back_to_menu']]
            )
        ])

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    @staticmethod
    def interior_upgrade_plan() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['interior_choose_plan'],
                                      callback_data=callbacks[buttons['interior_choose_plan']])],
                [InlineKeyboardButton(text=buttons['back_to_menu'],
                                      callback_data=callbacks[buttons['back_to_menu']])]
            ]
        )

        return kb

    @staticmethod
    def dress_up_upgrade_plan() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['dress_up_choose_plan'],
                                      callback_data=callbacks[buttons['dress_up_choose_plan']])],
                [InlineKeyboardButton(text=buttons['back_to_menu'],
                                      callback_data=callbacks[buttons['back_to_menu']])]
            ]
        )

        return kb
