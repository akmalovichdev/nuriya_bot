from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
import os
import logging
import db

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1002175722641
CHANNEL_ID = -1002198604799
ADMIN_ID = 7055308233

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Register(StatesGroup):
    message = State()

current_date = datetime.now().strftime("%Y-%m-%d")

@dp.message_handler(content_types=[ContentType.PHOTO])
async def handle_photo(message: types.Message):
    if message.chat.id != GROUP_ID:
        return
    photo = message.photo[-1]
    try:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo.file_id,
            caption=f"🆕 Yangi mahsulot {current_date} \n\n📌 Nuriya pastels\n\nSayt: nuriyapastels.netlify.app\nTelegramBot: @nuriyapastels_bot\nTelegram guruh: @nuriya_pastels_n1\nAdmin: @nuriya_pastels_2024"
        )
    except Exception as e:
        print(f"Error sending photo: {e}")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if not db.exist.user(message.from_user.id):
        db.add.user(message.from_user.id, message.from_user.full_name)

    menu = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton(text="Xabar yuborish", callback_data='register')
    button3 = InlineKeyboardButton(text='Kanal', url='https://t.me/@nuriyapastels')
    button4 = InlineKeyboardButton(text='Guruh', url='https://t.me/nuriya_pastels_n1')
    button5 = InlineKeyboardButton(text='Mini ilova', url='https://t.me/nuriyapastels_bot/Nuriya')
    menu.add(button2).add(button3).add(button4).add(button5)

    await bot.send_message(message.from_user.id, f'Salom {message.from_user.full_name}, Nuriya pastels ga xush kelibsiz', reply_markup=menu)

@dp.callback_query_handler(text='register')
async def message_handler(callback_query: types.CallbackQuery, state: FSMContext):
    menu = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Orqaga⬅️', callback_data='back')
    menu.add(button1)
    
    await bot.send_message(callback_query.from_user.id, "Iltimos, xabaringizni yozing", reply_markup=menu)
    await Register.message.set()

@dp.message_handler(state=Register.message)
async def result_handler(msg: types.Message, state: FSMContext):
    await state.update_data(message=msg.text)
    data = await state.get_data()
    await bot.send_message(
        msg.from_user.id,
        f"Rahmat! {msg.from_user.full_name}, sizning habaringiz muvaffaqiyatli yuborildi."
    )
    await bot.send_message(
        ADMIN_ID,
        f"Ismi: {msg.from_user.full_name}\nFoydalanuvchi: @{msg.from_user.username}\nXabari: {data['message']}"
    )
    await state.finish()

@dp.callback_query_handler(text='back', state=Register.message)
async def back_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()

    menu = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton(text="Xabar yuborish", callback_data='register')
    button3 = InlineKeyboardButton(text='Kanal', url='https://t.me/@nuriyapastels')
    button4 = InlineKeyboardButton(text='Guruh', url='https://t.me/nuriya_pastels_n1')
    button5 = InlineKeyboardButton(text='Mini ilova', url='https://t.me/nuriyapastels_bot/Nuriya')
    menu.add(button2).add(button3).add(button4).add(button5)

    await bot.send_message(callback_query.from_user.id, "Asosiy menyuga qaytdingiz", reply_markup=menu)

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome_new_members(message: types.Message):
    logging.info(f"New member joined: {message.new_chat_members}")
    if message.chat.id == GROUP_ID:
        for new_member in message.new_chat_members:
            welcome_message = f"Xush kelibsiz, {new_member.full_name}! Nuriya pastels guruhiga a'zo bo'lganingiz uchun rahmat."
            
            menu = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton(text='Bot bilan tanishish', url=f'https://t.me/nuriyapastels_bot')
            menu.add(button1)
            
            await message.reply(welcome_message, reply_markup=menu)

async def on_startup(_):
    print('Bot ishlayapti...')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)