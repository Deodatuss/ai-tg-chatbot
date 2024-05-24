from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State

from state_class import GenerationStages

router = Router()


@router.message(Command("my_tokens"))
async def tokens_on_account():
    """
    Output: message with how much tokens left on account
    Autosends after every generation
    """
    pass


@router.message(Command("buy_tokens"))
async def buy_tokens():
    """
    Uses inline buttons to choose how much tokens to buy.
    Currently buttons are stubs for payment, and directly add tokens instead
    """
    pass
