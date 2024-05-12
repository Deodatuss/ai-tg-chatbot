# V4
import torch
import torchaudio
import asyncio
import logging
import sys


LANG = "ru"
MODEL_ID = "v4_ru"
SAMPLE_RATE = 24000  # should be in [8000, 24000, 48000]
SPEAKER = "xenia"
DEVICE = torch.device("cuda")

# backend = torchaudio.utils.ffmpeg_utils.get_audio_encoders()
# print(backend)


async def load_model(language=LANG, model_id=MODEL_ID, device=DEVICE):
    model, example_text = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_tts",
        language=language,
        speaker=model_id,
    )
    model.to(device)
    print("loaded")
    return model, example_text


async def inference_tts(
    model, text="В н+едрах т+ундры в+ыдры", speaker=SPEAKER, sample_rate=SAMPLE_RATE
) -> str:
    """
    Input: loaded TTS model object
    Output: path of a saved audio file

    Saves the file with torchaudio.save inside /data/{user_id_number}/generated/{user_id}_{file_id}.mp3
    ; use another function to read the audio file
    """
    audio = model.apply_tts(
        text=text,
        speaker=speaker,
        sample_rate=SAMPLE_RATE,
    )

    file_uri = "./example_saved3.mp3"

    torchaudio.save(
        uri=file_uri,
        src=torch.unsqueeze(audio, 0),
        sample_rate=SAMPLE_RATE,
        backend="soundfile",
    )

    return file_uri


async def main() -> None:
    model, example_text = await load_model()
    file_uri = await inference_tts(model)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
