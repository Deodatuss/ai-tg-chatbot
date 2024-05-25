import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Router, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_list


import silero_tts
import inference_router, tokens_router, db_handler

from config_reader import config
from state_class import GenerationStages

TOKEN = config.bot_token.get_secret_value()

base_router = Router()


@base_router.message(CommandStart(), StateFilter(None))
async def start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}! This bot can convert text messages into audio messages"
    )

    await load_account(message, state)

    await state.update_data(chosen_model=None)
    await state.update_data(model_language=None)
    await state.update_data(audio_uri=None)
    await state.set_state(GenerationStages.setting_parameters)


async def load_account(message: Message, state: FSMContext) -> None:
    if await db_handler.is_existing_user(message, state):
        await db_handler.load_user_info_to_state(message, state)
    else:
        await db_handler.add_new_user_to_df(message, state)
        await db_handler.load_user_info_to_state(message, state)


@base_router.message(StateFilter(None))
async def warn_to_start(message: Message) -> None:
    await message.answer("Try to start the bot first with /start.")


@base_router.message(CommandStart())
async def start_doubled(message: Message, state: FSMContext) -> None:
    await message.answer(f"You've already started the bot")


@base_router.message(Command("ua_model"), GenerationStages.setting_parameters)
async def choose_ukr_model(message: Message, state: FSMContext):
    await message.answer("Loading ukrainian language model")
    new_model, _ = await silero_tts.load_model(language="ua", model_id="v4_ua")
    await state.update_data(chosen_model=new_model)
    await state.update_data(model_language="ua")
    await message.answer(
        "Ukraininan model loaded. Use /read to get into generation mode"
    )


@base_router.message(Command("en_model"), GenerationStages.setting_parameters)
async def choose_eng_model(message: Message, state: FSMContext):
    await message.answer("Loading english language model")
    new_model, _ = await silero_tts.load_model(language="en", model_id="v3_en")
    await state.update_data(chosen_model=new_model)
    await state.update_data(model_language="en")
    await message.answer("English model loaded. Use /read to get into generation mode")


@base_router.message(Command("info"))
async def show_user_parameters(message: Message, state: FSMContext):
    user_data = await state.get_data()
    info = [
        f"Model language: {user_data['model_language']}.",
        f"Your Tokens: {user_data['my_tokens']}",
        f"Generations made: {user_data['my_gens']}",
    ]

    text = as_list(*info)
    await message.answer(**text.as_kwargs())


@base_router.message(Command("help"))
async def help_answer(message: Message, state: FSMContext):
    info = [
        "Current available models:",
        "ukrainian, chosen with /ua_model",
        "english, chosen with /en_model",
        "",
        "After choosing a model, use /read command to start one-message Generation mode. "
        + "In this mode, your next text message will be read by the bot, and he will reply with audio soon.",
        "This mode ends after one text message or after /stop. After that, you can change AI model, or use token commands.",
        "",
        "Help section still in progress. Don't mess up with a bot and no one will be hurt",
        "(including the bot itself: he will agonize with errors)",
    ]
    text = as_list(*info)
    await message.answer(**text.as_kwargs())


@base_router.message()
async def wildcard_answer(message: Message, state: FSMContext):
    await message.answer(
        "I don't know how to respond... I either don't work with such message types, or command is not proper right now. "
        + "See /help for more info.",
    )
    await message.answer(f"Btw, your state is {await state.get_state()}")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And then run events dispatching
    dp = Dispatcher()
    dp.include_routers(
        inference_router.router,
        tokens_router.router,
        base_router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
