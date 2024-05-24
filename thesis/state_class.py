from aiogram.fsm.state import StatesGroup, State


class GenerationStages(StatesGroup):
    setting_parameters = State()  # starter and general state
    inference_mode = State()
    choosing_payment = State()
