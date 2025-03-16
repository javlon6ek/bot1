import sqlite3
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

CHANNEL_ID = -1002270307680
ADMIN_ID = 6167775229
bot = Bot(token="6627165983:AAENQMQksSrzfCxZ9ECcuuQsJsA5rIPPZ90")
dp = Dispatcher()


conn = sqlite3.connect("buttons.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS buttons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        button_name TEXT,
        message_id INTEGER
    )
""")
conn.commit()


class AddButton(StatesGroup):
    waiting_for_button_name = State()

class DeleteButton(StatesGroup):
    waiting_for_button_selection = State()

class AddMessage(StatesGroup):
    waiting_for_button_selection = State()
    waiting_for_message = State()


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Tugma qo‘shish")],
        [KeyboardButton(text="Tugma o‘chirish")],
        [KeyboardButton(text="Xabar qo‘shish")]
    ],
    resize_keyboard=True
)


stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="To‘xtatish")]
    ],
    resize_keyboard=True
)

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=admin_keyboard)
    else:
        await message.answer("Siz admin emassiz!")

@dp.message(lambda message: message.text == "Tugma qo‘shish")
async def process_add_button(message: types.Message, state: FSMContext):
    await message.answer("Yangi tugma nomini yuboring:")
    await state.set_state(AddButton.waiting_for_button_name)

@dp.message(AddButton.waiting_for_button_name)
async def save_button_name(message: types.Message, state: FSMContext):
    button_name = message.text
    try:
        cursor.execute("INSERT INTO buttons (name) VALUES (?)", (button_name,))
        conn.commit()
        await message.answer(f"'{button_name}' nomli tugma qo‘shildi!",reply_markup=admin_keyboard)
    except sqlite3.IntegrityError:
        await message.answer("Bunday nomli tugma allaqachon mavjud!")
    await state.clear()

@dp.message(lambda message: message.text == "Tugma o‘chirish")
async def process_delete_button(message: types.Message, state: FSMContext):
    buttons = await get_buttons()
    if not buttons:
        await message.answer("Hech qanday tugma mavjud emas!")
        return
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button)] for button in buttons],
        resize_keyboard=True
    )
    await message.answer("O‘chirmoqchi bo‘lgan tugmangizni tanlang:", reply_markup=kb)
    await state.set_state(DeleteButton.waiting_for_button_selection)

@dp.message(DeleteButton.waiting_for_button_selection)
async def delete_selected_button(message: types.Message, state: FSMContext):
    button_name = message.text
    cursor.execute("DELETE FROM buttons WHERE name = ?", (button_name,))
    cursor.execute("DELETE FROM messages WHERE button_name = ?", (button_name,))
    conn.commit()
    await message.answer(f"'{button_name}' nomli tugma o‘chirildi!", reply_markup=admin_keyboard)
    await state.clear()

@dp.message(lambda message: message.text == "Xabar qo‘shish")
async def process_add_message(message: types.Message, state: FSMContext):
    buttons = await get_buttons()
    if not buttons:
        await message.answer("Hech qanday tugma mavjud emas!")
        return
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button)] for button in buttons],
        resize_keyboard=True
    )
    await message.answer("Qaysi tugmaga xabar qo‘shmoqchisiz?", reply_markup=kb)
    await state.set_state(AddMessage.waiting_for_button_selection)

@dp.message(AddMessage.waiting_for_button_selection)
async def receive_message_for_button(message: types.Message, state: FSMContext):
    await state.update_data(button_name=message.text)
    await message.answer("Endi xabar yuboring.")
    await state.set_state(AddMessage.waiting_for_message)

@dp.message(AddMessage.waiting_for_message)
async def save_message_for_button(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "to‘xtatish":
        await message.answer("Xabar qo‘shish yakunlandi.", reply_markup=admin_keyboard)
        await state.clear()
        return
    data = await state.get_data()
    button_name = data.get("button_name")
    sent_message = await bot.copy_message(chat_id=CHANNEL_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    cursor.execute("INSERT INTO messages (button_name, message_id) VALUES (?, ?)", (button_name, sent_message.message_id))
    conn.commit()
    await message.answer("Xabar saqlandi! Yana xabar yuborishingiz mumkin yoki 'To‘xtatish' tugmasini bosing.",reply_markup=stop)

async def get_buttons():
    cursor.execute("SELECT name FROM buttons")
    buttons = cursor.fetchall()
    return [button[0] for button in buttons]

@dp.message(Command("start"))
async def start_command(message: types.Message):
    start_param = message.text.split(' ')[-1]
    if start_param == "salom":
        await message.answer("Salom!")
 
    buttons = await get_buttons()
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button)] for button in buttons],
        resize_keyboard=True
    )
    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=kb)
    
@dp.message()
async def handle_button(message: types.Message) -> None:
    text: str = message.text

    cursor.execute("SELECT message_id FROM messages WHERE button_name = ?", (text,))
    result: tuple[int] | None = cursor.fetchone()

    if result is None:
        await message.answer("Bunaqa tugma mavjud emas")
        return

    message_id: int = result[0]

    await bot.copy_message(
        chat_id=message.chat.id, from_chat_id=CHANNEL_ID, message_id=message_id
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
