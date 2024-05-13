import asyncio
import logging
import sys
from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods.send_voice import SendVoice

import silero_tts, tokenizer

from config_reader import config

TOKEN = config.bot_token.get_secret_value()
dp = Dispatcher()
DATA_PATH = Path("data/tts/")


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await state.update_data(chosen_model=None)
    await state.update_data(model_language=None)
    await state.update_data(audio_uri=None)


@dp.message(Command("my_tokens"))
async def tokens_on_account():
    """
    Output: message with how much tokens left on account
    Autosends after every generation
    """
    pass


@dp.message(Command("buy_tokens"))
async def buy_tokens():
    """
    Uses inline buttons to choose how much tokens to buy.
    Currently buttons are stubs for payment, and directly add tokens instead
    """
    pass


@dp.message(Command("resend"))
async def reply_output(
    message: Message,
    state: FSMContext,
):
    """
    Looks for proper folder and gets the file with the last file_id
    Reads audio file and sends file message to the user
    """
    user_data = await state.get_data()
    audio_from_pc = FSInputFile(user_data["audio_uri"])
    await message.answer_voice(audio_from_pc)
    return


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


@dp.message(Command("read"))
async def read_text_with_tts(
    message: Message,
    state: FSMContext,
    command: CommandObject,
):
    """
    I thought to make it a state machine with waiting another input after a command;
    think it's just easier instead to process any text after the "/read" as the input text.
    Checks if there is enough tokens on the account; alerts if doesn't.
    If enough, takes away tokens and does inference, then itself answers with reply_output
    """
    user_data = await state.get_data()
    model = user_data["chosen_model"]
    speaker = "random"
    if user_data["model_language"] == "en":
        speaker = "en_0"
    elif user_data["model_language"] == "ua":
        speaker = "mykyta"

    # TODO: index new files and create new file for each generation
    file_path = DATA_PATH / Path(str(message.from_user.id))
    file_path.mkdir(parents=True, exist_ok=True)

    await message.answer("Started reading")
    audio_uri = await silero_tts.inference_tts(
        model=model,
        path=file_path,
        text=command.args,
        speaker=speaker,
    )
    await message.answer("Done")

    await state.update_data(audio_uri=audio_uri)
    await reply_output(message, state)
    return


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
