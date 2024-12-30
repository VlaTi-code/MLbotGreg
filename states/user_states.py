from aiogram.fsm.state import State, StatesGroup, default_state


class UserState(StatesGroup):
    default_state = default_state

    waiting_for_model_name = State()
    waiting_for_photos = State()

    choosing_model = State()

    choosing_plan = State()
