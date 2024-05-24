from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from state_class import GenerationStages

import tokenizer

router = Router()


@router.message(Command("my_tokens"))
async def tokens_on_account(message: Message, state: FSMContext):
    """
    Output: message with how much tokens left on account
    Autosends after every generation
    """
    pass


@router.message(Command("buy_tokens"))
async def buy_tokens(message: Message, state: FSMContext):
    """
    Uses inline buttons to choose how much tokens to buy.
    Currently buttons are stubs for payment, and directly add tokens instead
    """
    pass
