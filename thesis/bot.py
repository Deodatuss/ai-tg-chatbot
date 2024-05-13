import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import silero_tts, tokenizer

from config_reader import config

TOKEN = config.bot_token.get_secret_value()
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command())
async def tokens_on_account():
    """
    Output: message with how much tokens left on account
    Autosends after every generation
    """
    pass


@dp.message()
async def buy_tokens():
    """
    Uses inline buttons to choose how much tokens to buy.
    Currently buttons are stubs for payment, and directly add tokens instead
    """
    pass


@dp.message()
async def reply_output():
    """
    Looks for proper folder and gets the file with the last file_id
    Reads audio file and sends file message to the user
    """
    pass


@dp.message(Command())
async def choose_ukr_model():
    pass


@dp.message(Command())
async def choose_eng_model():
    """
    ability to choose from eng or ukr models;
    replies twice, with "loading eng/ukr model" and "loaded"
    """
    pass


@dp.message(Command("read"))
async def read_text_with_tts():
    """
    I thought to make it a state machine with waiting another input after a command;
    think it's just easier instead to process any text after the "/read" as the input text.
    Checks if there is enough tokens on the account; alerts if doesn't.
    If enough, takes away tokens and does inference, then itself answers with reply_output
    """
    pass


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
