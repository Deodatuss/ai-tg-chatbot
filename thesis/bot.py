import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import silero_tts, tokenizer

from config_reader import config
from state_class import GenerationStages

TOKEN = config.bot_token.get_secret_value()
dp = Dispatcher()


@dp.message(CommandStart() and StateFilter(None))
async def start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await state.update_data(chosen_model=None)
    await state.update_data(model_language=None)
    await state.update_data(audio_uri=None)
    await state.set_state(GenerationStages.setting_parameters)


@dp.message(Command("ua_model"))
async def choose_ukr_model(message: Message, state: FSMContext):
    await message.answer("Loading ukrainian language model")
    new_model, _ = await silero_tts.load_model(language="ua", model_id="v4_ua")
    await state.update_data(chosen_model=new_model)
    await state.update_data(model_language="ua")
    await message.answer("Ukraininan model loaded")


@dp.message(Command("en_model"))
async def choose_eng_model(message: Message, state: FSMContext):
    await message.answer("Loading english language model")
    new_model, _ = await silero_tts.load_model(language="en", model_id="v3_en")
    await state.update_data(chosen_model=new_model)
    await state.update_data(model_language="en")
    await message.answer("English model loaded")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
