from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F


router = Router()


user_models = {}

models_menu = [
    [InlineKeyboardButton(text = 'Deepseek-chat', callback_data = 'model_deepseek')],
    [InlineKeyboardButton(text = 'Gigachat', callback_data = 'model_gigachat')],
    [InlineKeyboardButton(text = 'Mistral', callback_data = 'model_mistral')],   
]

models_menu = InlineKeyboardMarkup(inline_keyboard = models_menu)


@router.callback_query(F.data == "choose_model")
async def choose_model_handler(callback: CallbackQuery):
    await callback.message.answer('Выберите желаемую модель из представленных: ', reply_markup=models_menu)
    await callback.answer()

@router.callback_query(F.data.startswith("model_"))
async def model_handler(callback: CallbackQuery):
    model_name = callback.data.replace("model_", '')
    if model_name == 'deepseek':
        user_models[callback.from_user.id] = "deepseek-chat"
    elif model_name == 'gigachat':
        user_models[callback.from_user.id] = 'GigaChat-Pro'
    elif model_name == 'mistral':
        user_models[callback.from_user.id] = 'mistral-large-latest'

    await callback.message.answer(
        f"✅Вы выбрали модель: {user_models[callback.from_user.id]}. Замечательный выбор! Скорее задайте мне вопрос"
    )
    await callback.answer()

