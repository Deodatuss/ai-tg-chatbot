from pathlib import Path


from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


import silero_tts, tokenizer, constants, db_handler
from state_class import GenerationStages

router = Router()
DATA_PATH = constants.DATA_PATH


@router.message(Command("read"), GenerationStages.setting_parameters)
async def get_ready_for_inference(message: Message, state: FSMContext):
    user_data = await state.get_data()

    if user_data["model_language"] is None:
        await message.answer("Please choose a model first. Use /help for more info")
        return

    await message.answer(
        "Generation mode started. Send text message you want to read. Or /stop to stop."
    )
    await state.set_state(GenerationStages.inference_mode)
    return


@router.message(Command("stop"), GenerationStages.inference_mode)
async def stop_inference(message: Message, state: FSMContext):
    await message.answer("Generation mode stopped.")
    await state.set_state(GenerationStages.setting_parameters)


@router.message(F.text, GenerationStages.inference_mode)
async def check_tokens_and_params_then_read(message: Message, state: FSMContext):
    text_tokens = await tokenizer.count_tokenize_message(message, state)
    is_enough = await tokenizer.is_enough_tokens(state, text_tokens)
    user_tokens = await tokenizer.get_tokens(state)

    if is_enough:
        # negative value for text_tokens, as it's abducting them from balance
        await tokenizer.update_tokens(message.from_user, state, -text_tokens)
        await read_text_with_tts(message, state)
    else:
        await message.answer(
            f"Not enough tokens; You have {user_tokens} tokens but need {text_tokens} tokens. "
            + "Leaving generation mode",
        )
    await state.set_state(GenerationStages.setting_parameters)
    return


async def read_text_with_tts(message: Message, state: FSMContext):
    """
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

    await message.answer("Started reading. Please, wait")
    try:
        audio_uri = await silero_tts.inference_tts(
            model=model,
            path=file_path,
            text=message.text,
            speaker=speaker,
        )
    except ValueError:
        await message.answer(
            "AI model expirienced a value error. "
            + "Your input message may have bad characters, "
            + "or message language is not supported by chosen "
            + f"{user_data['model_language']} model",
        )
    else:
        await db_handler.increment_generations_for_user(message, state)

        await state.update_data(audio_uri=audio_uri)
        await reply_output(message, state)
    return


@router.message(GenerationStages.inference_mode)
async def wrong_input(
    message: Message,
    state: FSMContext,
):
    await message.answer(
        "Wrong input. Try to send simple text or send /stop command to stop."
    )


@router.message(Command("resend"))
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
