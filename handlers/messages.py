import logging
import os

from aiogram import types, Router
from aiogram.enums import ChatAction
from services.ai_service import AIService
from services.history_manager import HistoryManager
from dotenv import load_dotenv
from utils.split_text import split_text

logger = logging.getLogger(__name__)
router = Router()
load_dotenv()

yandex_id = os.getenv('YANDEX_ID')
yandex_key = os.getenv('YANDEX_KEY')
yandex_bucket = os.getenv('YANDEX_BUCKET')
endpoint = os.getenv('ENDPOINT')
max_messages = int(os.getenv('MAX_HISTORY_MESSAGES', '20'))


ai_service = AIService()
history_manager = HistoryManager(yandex_bucket)
user_models = {}

@router.message()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    model = user_models.get(message.from_user.id, 'mistral-large-latest')
    
    try:
        history = await history_manager.add_message(
            chat_id, 
            "user", 
            message.text,
            max_messages=max_messages
        )
        
        await message.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING
        )
        
        response = await ai_service.get_response(model, history)
        
        await history_manager.add_message(
            chat_id,
            "assistant",
            response,
            max_messages=max_messages
        )

        parts = split_text(response, 4000)

        await message.reply(parts[0])
        for part in parts[1:]:
            await message.answer(part)   

    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await message.reply("❌ Произошла ошибка. Попробуйте снова.")