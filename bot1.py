from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio

TOKEN = '6627165983:AAENQMQksSrzfCxZ9ECcuuQsJsA5rIPPZ90'
ADMIN_ID = 6167775229


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("salom")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

