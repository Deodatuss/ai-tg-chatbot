from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.callback_query import CallbackQuery


import tokenizer
from state_class import GenerationStages


router = Router()


@router.message(Command("my_tokens"), GenerationStages.setting_parameters)
async def tokens_on_account(message: Message, state: FSMContext):
    """
    Output: message with how much tokens left on account
    Autosends after every generation
    """
    user_data = await state.get_data()
    tokens = user_data["my_tokens"]
    await message.answer(f"You have {tokens} tokens")


@router.message(Command("buy_tokens"), GenerationStages.setting_parameters)
async def buy_tokens(message: Message, state: FSMContext):
    """
    Uses inline buttons to choose how much tokens to buy.
    Currently buttons are stubs for payment, and directly add tokens instead
    """
    kb = [
        [
            InlineKeyboardButton(text="10 tokens – 0.1 $", callback_data="tokens-10"),
            InlineKeyboardButton(text="100 tokens – 1 $", callback_data="tokens-100"),
            InlineKeyboardButton(text="1000 tokens – 8 $", callback_data="tokens-1000"),
        ],
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(
        "Choose how much tokens to get",
        reply_markup=ikb,
    )


@router.callback_query(F.data.startswith("tokens-"))
async def recieve_tokens(callback: CallbackQuery, state: FSMContext):
    data: str = callback.data
    tokens = int(data.split("-")[1])
    await callback.message.edit_text(
        f"You just recieved {tokens} tokens. " + "check your balance with /my_tokens"
    )
    await tokenizer.update_tokens(callback.from_user, state, tokens)
