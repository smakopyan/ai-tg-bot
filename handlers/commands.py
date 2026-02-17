from aiogram import Dispatcher, types
from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()


menu = [
    [InlineKeyboardButton(text = '📝 Генерировать текст', callback_data='handler'),
     InlineKeyboardButton(text = '🖼 Генерировать изображение', callback_data= 'handler')],
    [InlineKeyboardButton(text = '🤖 Выбор модели', callback_data= 'choose_model')],
    [InlineKeyboardButton(text = '💰 Поддержка админу 💰', url='https://halvamedia.sovcombank.ru/68765/cropped-Airbrush.jpg')],
    [InlineKeyboardButton(text = '💎 Партнёрская программа 💎', url='https://halvamedia.sovcombank.ru/68765/cropped-Airbrush.jpg')],
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)



@router.message(Command('menu'))
async def menu_handler(message: types.Message):
    await message.answer('Выберите в меню подходящую опцию: ', reply_markup=menu)

@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer('Привет! Я ваш новый ИИ-ассистент! Отправьте мне любое сообщение и я с удовольствием отвечу на него :)')

@router.message(Command('help'))
async def help_handler(message: types.Message):
    # TODO
    await message.answer('Для получения помощи по любому вопросу, обращайтесь по следующему адресу: ')
