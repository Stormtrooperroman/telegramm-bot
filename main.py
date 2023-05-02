from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


BOT_TOKEN: str = '6070150264:AAExDUSmdR_M8V_n-pFEFIEM1MclOrSe5Y4'

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='___Пример форматированного текста_\r__',
                       parse_mode='HTML')




if __name__ == '__main__':
    dp.run_polling(bot)
