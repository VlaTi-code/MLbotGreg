LEXICON: dict[str, str | list[str]] = {
    'start': '<b>Генератор фото с ИИ LORA AI</b>\n\n'
             'Представьте, что вы можете встроить любой предмет в любой интерьер или посмотреть, '
             'как выглядит любой предмет одежды на любом человеке.\n\n'
             'LORA воплощает это в жизнь!\n\n'
             'Выберите режим на клавиатуре',
    'interior_regime_intro': '<b>Как это работает?</b>\n\n'
                             '1. Вы создаете модель и называете ее как предмет, '
                             'с которым вы собираетесь генерировать изображения '
                             '(например: белый стул - White сhair, спортивная сумка - Sports bag)\n'
                             '2. Вы загружаете от 7 до 10 фотографий предмета <b>одним сообщением</b>. '
                             'После этого начинается процесс обучения модели (от 10 до 20 минут)'
                             '3. Когда модель обучена, вы можете генерировать '
                             'изображения с этим предметов по вашему запросу! '
                             '(например "<b>White chair</b> in the center of the dining room" или '
                             '"<b>Sports bag</b> lies on a lounger near the swimming pool")',
    'interior_new_model_enter_model_name': '<b>Напишите название новой модели</b>',
    'interior_new_model_enter_photos': 'Отлично! Теперь загрузите от <b>7 до 10 фотографий</b> '
                                       'предмета для обучения модели <code>{}</code> <b>одним сообщением</b>',
    'interior_new_model_enter_photos_successful': 'Процесс обучения начался. '
                                                  'Скоро модель появится в доступных для генерации.',
    'interior_new_model_enter_photos_failed_not_enough_photos': 'Недостаточно фотографий, пожалуйста, '
                                                                'прикрепите 7-10 фото к одному сообщению и '
                                                                'отправьте боту для обучения',
    'interior_gen_with_existing_model': 'Выберите модель с которой вы будете генерировать фотографии:',
    'interior_choose_plan': '<b>Выберите план:</b>\n\n'
                            '<b>Interior Standard:</b> 3 обучения модели + 30 генераций - 2199р\n'
                            '<b>Interior Pro:</b> 5 обучений модели + 50 генераций - 3199р\n'
                            '<b>Interior Premium:</b> 10 обучений модели + 100 генераций - 5999р\n',

    'dress_up_regime_intro': '<b>Как это работает?</b>\n\n'
                             'Вы можете легко посмотреть, как выглядит предмет одежды на любом человеке!\n'
                             'Механизм работы прост:'
                             '1. Вы отправляете нам 2 фотографии: предмета одежды и человека, '
                             'на которого вы хотите примерить одежду\n'
                             '2. Мы возвращаем вам результат примерки\n\n'
                             'Вам доступно 20 пробных генераций:',
    'dress_up_choose_plan': '<b>Выберите план:</b>\n\n'
                            '<b>Dress up Standard:</b> 50 генераций в месяц - 700р\n'
                            '<b>Dress up Pro:</b> 100 генераций в месяц - 1000р\n'
                            '<b>Dress up Premium:</b> 300 генераций в месяц - 2500р\n',

    'help': 'Обратиться за помощью: <code>{}</code>'
}

buttons: dict[str, str] = {
    'interior_regime': 'Встроить предмет в интерьер',
    'interior_new_model': 'Создать новую модель',
    'interior_gen_with_existing_model': 'Сгенерировать изображение с существующей моделью',
    'interior_choose_plan': 'Выбрать тариф',

    'interior_standard': 'Interior Standard',
    'interior_pro': 'Interior Pro',
    'interior_premium': 'Interior Premium',

    'dress_up_regime': 'Примерить одежду',
    'dress_up_new_gen': 'Сгенерировать изображение',
    'dress_up_choose_plan': 'Выбрать тариф',

    'dress_up_standard': 'Dress up Standard',
    'dress_up_pro': 'Dress up Pro',
    'dress_up_premium': 'Dress up Premium',

    'back_to_menu': 'Назад в меню',
    'help': 'Помощь',
}

callbacks: dict[str, str] = {
    buttons['interior_regime']: 'interior_regime_button',
    buttons['interior_new_model']: 'interior_new_model_button',
    buttons['interior_gen_with_existing_model']: 'interior_gen_with_existing_model_button',
    buttons['interior_choose_plan']: 'interior_choose_plan_button',

    buttons['interior_standard']: 'interior_standard_button',
    buttons['interior_pro']: 'interior_pro_button',
    buttons['interior_premium']: 'interior_premium_button',

    buttons['dress_up_regime']: 'dress_up_regime_button',
    buttons['dress_up_new_gen']: 'dress_up_new_gen_button',
    buttons['dress_up_choose_plan']: 'choose_plan_button',

    buttons['dress_up_standard']: 'dress_up_standard_button',
    buttons['dress_up_pro']: 'dress_up_pro_button',
    buttons['dress_up_premium']: 'dress_up_premium_button',

    buttons['back_to_menu']: 'back_to_menu_button',
    buttons['help']: 'help_button',
}

# status_callback_to_string: dict[str, str] = {
#     'registration_status_bachelor-cu': buttons['registration_status_bachelor-cu'],
#     'registration_status_master-cu': buttons['registration_status_master-cu'],
#     'registration_status_other': buttons['registration_status_other']
# }
