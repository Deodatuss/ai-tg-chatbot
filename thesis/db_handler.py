from pandas import Timestamp

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database

router = Router()


async def add_new_user_to_df(message: Message, state: FSMContext) -> None:
    new_user = {
        "uid": [int(message.from_user.id)],
        "uname": [str(message.from_user.full_name)],
        "added": [Timestamp.today()],
        "tokens": [0],
        "generations": [0],
    }
    database.add_user_entry(new_user)


async def is_existing_user(message: Message, state: FSMContext) -> bool:
    return database.is_existing_user(message.from_user.id)


async def load_user_info_to_state(message: Message, state: FSMContext) -> bool:
    await state.update_data(
        my_tokens=database.get_tokens_by_id(message.from_user.id),
    )
    await state.update_data(
        my_gens=database.get_gens_by_id(message.from_user.id),
    )
