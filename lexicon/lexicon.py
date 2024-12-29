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

    'dress_up_regime_intro': '<b>Как это работает?</b>\n\n'
                            'Вы можете легко посмотреть, как выглядит предмет одежды на любом человеке!\n'
                            'Механизм работы прост:'
                            '1. Вы отправляете нам 2 фотографии: предмета одежды и человека, '
                            'на которого вы хотите примерить одежду\n'
                            '2. Мы возвращаем вам результат примерки\n\n'
                            'Вам доступно 20 пробных генераций:',

    'help': 'Обратиться за помощью: @IT4shnik'
}

buttons: dict[str, str] = {
    'interior_regime': 'Встроить предмет в интерьер',
    'interior_new_model': 'Создать новую модель',
    'interior_gen_with_existing_model': 'Сгенерировать изображение с существующей моделью',
    'interior_choose_plan': 'Выбрать тариф',

    'dress_up_regime': 'Примерить одежду',
    'dress_up_new_gen': 'Сгенерировать изображение',
    'dress_up_choose_plan': 'Выбрать тариф',

    'back_to_menu': 'Назад в меню',
    'help': 'Помощь',
}

callbacks: dict[str, str] = {
    buttons['interior_regime']: 'interior_regime_button',
    buttons['interior_new_model']: 'interior_new_model_button',
    buttons['interior_gen_with_existing_model']: 'interior_gen_with_existing_model_button',
    buttons['interior_choose_plan']: 'interior_choose_plan_button',

    buttons['dress_up_regime']: 'dress_up_regime_button',
    buttons['dress_up_new_gen']: 'dress_up_new_gen_button',
    buttons['dress_up_choose_plan']: 'choose_plan_button',

    buttons['back_to_menu']: 'back_to_menu_button',
    buttons['help']: 'help_button',
}

# status_callback_to_string: dict[str, str] = {
#     'registration_status_bachelor-cu': buttons['registration_status_bachelor-cu'],
#     'registration_status_master-cu': buttons['registration_status_master-cu'],
#     'registration_status_other': buttons['registration_status_other']
# }
