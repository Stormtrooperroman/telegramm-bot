import subprocess
import wave
import io
import json

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import BufferedInputFile
import numpy
import redis

from TTS import tts
from conf import BOT_TOKEN
from dialogue import dialogue

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


redis_db = redis.Redis(host='redis', port=6379, decode_responses=True)


def write_wave(audio: numpy.ndarray, sample_rate: int):
    """
    Конвертирует numpy.ndarray в wav формат.
    :arg audio: numpy.ndarray # массив описывающий аудио
    :arg sample_rate: int # частота дискретизации аудио файла
    :return
    """
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

@dp.message(Command(commands=["clear"]))
async def process_clear_command(message: Message):
    redis_db.delete(f"{message.chat.id}")
    await message.answer('История очищенна.')

@dp.message()
async def send_msg(message: Message):
    if message.text is not None and message.text != "":
        history = []
        if redis_db.exists(f"message.chat.id"):
            history = json.loads(redis_db.get(f"{message.chat.id}"))
        history = dialogue(message.text, history)
        redis_db.set(f"{message.chat.id}", json.dumps(history))
        audio = tts(history[-1][1])
        audio_wav = write_wave(audio=(audio * 32767).numpy().astype('int16'),
                    sample_rate=48000)
        audio_ogg = wav_to_ogg_bytes(audio_wav)
        voice = BufferedInputFile(audio_ogg, "ogg_voice")

        await message.reply_voice(voice)


if __name__ == '__main__':
    print("Start bot!")
    dp.run_polling(bot)
