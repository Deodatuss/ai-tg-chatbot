from pathlib import Path


from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject


import silero_tts
from state_class import GenerationStages

router = Router()
DATA_PATH = Path("data/tts/")


@router.message(GenerationStages.inference_mode, Command("stop"))
async def stop_inference(
    message: Message,
    state: FSMContext,
):
    message.reply("Inference mode stopped.")
    state.set_state(GenerationStages.setting_parameters)


@router.message(GenerationStages.inference_mode, F.text)
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

    await message.answer("Started reading")
    audio_uri = await silero_tts.inference_tts(
        model=model,
        path=file_path,
        text=message.text,
        speaker=speaker,
    )
    await message.answer("Done")

    await state.update_data(audio_uri=audio_uri)
    await reply_output(message, state)
    return


@router.message(GenerationStages.inference_mode)
async def wrong_input(
    message: Message,
    state: FSMContext,
):
    message.reply("Wrong input. Try to send simple text or send /stop command to stop.")


@router.message(Command("read"), GenerationStages.setting_parameters)
async def get_ready_for_inference(
    message: Message,
    state: FSMContext,
):
    message.reply("Send text message you want to read.")
    state.set_state(GenerationStages.inference_mode)


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
