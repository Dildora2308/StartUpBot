from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils import executor
import asyncio
import logging
import sys
from dotenv import load_dotenv
from database import insert_data_database
from dotenv import load_dotenv
import os
load_dotenv()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()

def reply_buttons():
    kbs = [
        [types.KeyboardButton(text='/help')],[types.KeyboardButton(text='/StartUP idea yuborish')],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)
    return keyboard

@dp.message(CommandStart())
async def start_button(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.first_name}", reply_markup=reply_buttons())

class StartUp(StatesGroup):
    full_name = State()
    phone_number = State()
    project = State()

@dp.message(Command("StartUP idea yuborish"))
async def start(message: types.Message, state: FSMContext):
    await message.answer(text="Ism kiriting:")
    await state.set_state(StartUp.full_name)

@dp.message(StateFilter(StartUp.full_name))
async def take_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(text="Telefon raqam kiriting:")
    await state.set_state(StartUp.phone_number)

@dp.message(StateFilter(StartUp.phone_number))
async def take_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer(text="Yonalish nomi:")
    await state.set_state(StartUp.project)

@dp.message(StateFilter(StartUp.project))
async def describe_project(message: types.Message, state: FSMContext):  
    user_data = await state.get_data()
    
    
    insert_data_database(user_data['full_name'], user_data['phone_number'], message.text, user_data['project'])
    
    await message.answer(f"Ma'lumotlaringiz qabul qilindi:\n"
                         f"Ism: {user_data['full_name']}\n"
                         f"Telefon raqam: {user_data['phone_number']}\n"
                         f"Loyiha ma'lumotlari: {user_data['project']}")
    
    await state.clear() 

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":  
    asyncio.run(main())

