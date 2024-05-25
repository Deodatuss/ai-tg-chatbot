import logging


from bpemb import BPEmb
from aiogram.types import Message, User
from aiogram.fsm.context import FSMContext


import database

bpemb_en = BPEmb(lang="en", vs=10000)
bpemb_uk = BPEmb(lang="uk", vs=10000)


async def _set_tokens(user: User, state: FSMContext, tokens: int):
    """
    Setter of tokens for some user in a state and in database.
    """
    await state.update_data(my_tokens=tokens)
    database.set_tokens_by_id(user.id, tokens)
    return None


async def get_tokens(state: FSMContext):
    """
    Getter of tokens for some user from state.
    """
    user_data = await state.get_data()
    return user_data["my_tokens"]


async def is_enough_tokens(state: FSMContext, tokens_to_take: int):
    """
    Input: user id and number of tokens to take away.
    If available tokens are less then required, returns false.
    """
    if await get_tokens(state) >= tokens_to_take:
        return True
    return False


async def update_tokens(user: User, state: FSMContext, tokens_to_change: int):
    """
    Input: user id to be used as a key, and number of tokens to update
    sets tokens to be old value minus tokens used.
    Positive token values are added, e.g. from buying.
    Negative token values are taken from balance.
    """
    tokens = await get_tokens(state)
    new_tokens_count = tokens + tokens_to_change

    await _set_tokens(user, state, new_tokens_count)

    return None


async def count_tokenize_message(message: Message, state: FSMContext) -> int:
    """
    Returns list of strings which represent tokens.
    """
    user_data = await state.get_data()
    lang = user_data["model_language"]

    text = message.text

    if lang == "en":
        tokens: list = bpemb_en.encode(text)
        return len(tokens)

    if lang == "ua":
        tokens: list = bpemb_uk.encode(text)
        return len(tokens)

    message.answer("something went wrong with model language check")

    return 0
