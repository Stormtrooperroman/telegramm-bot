import subprocess
import wave
import io
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import BufferedInputFile
import numpy
# from transformers import AutoTokenizer, AutoModelForCausalLM

from TTS import tts
from conf import BOT_TOKEN


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


def write_wave(audio: numpy.ndarray, sample_rate: int):
    temp_file = io.BytesIO()
    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)
    temp_file.seek(0)
    return temp_file.read()


def wav_to_ogg_bytes(in_bytes: bytes) -> bytes:
    """
    Конвертирует аудио в ogg формат без сохранения данных на диск.

    :arg in_bytes: bytes  # входной файл в байтах
    :return:       bytes  # выходной файл в байтах
    """
    command = [
        'ffmpeg',
        "-i", 'pipe:0',          # stdin
        "-f", "ogg",             # format
        "-acodec", "libvorbis",  # codec
        "pipe:1"                 # stdout
    ]

    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out_bytes, err = proc.communicate(input=in_bytes)
    return out_bytes


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

@dp.message()
async def send_msg(message: Message):
    print(message.chat.id)
    if message.text is not None and message.text != "":
        audio = tts(message.text)
        audio_wav = write_wave(audio=(audio * 32767).numpy().astype('int16'),
                    sample_rate=48000)
        audio_ogg = wav_to_ogg_bytes(audio_wav)
        voice = BufferedInputFile(audio_ogg, "ogg_voice")

        await message.reply_voice(voice)


if __name__ == '__main__':
    print("HAAHHAAH")
    dp.run_polling(bot)
