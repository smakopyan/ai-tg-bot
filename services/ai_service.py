import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from groq import Groq
from mistralai import Mistral
from aiogram.enums import ChatAction
from gigachat import GigaChat
from openai import OpenAI


class AIService:
    def __init__(self):
        load_dotenv()

        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.gigachat_key = os.getenv("GIGACHAT_API_KEY")
        self.openai_api_key = os.getenv('OPEN_AI_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
            os.environ.pop(k, None)

        self.groq_client = Groq(api_key = self.groq_api_key) 
        self.deepseek_client = OpenAI(api_key=self.deepseek_key, base_url="https://api.deepseek.com", http_client=None)
        self.mistral_client = Mistral(api_key=self.mistral_key)


    async def get_response(self, model: str, messages: list[dict]) -> str:

        # model = user_models.get(message.from_user.id, 'mistral-large-latest')
        
        if model == 'mistral-large-latest':
            response = self.mistral_client.chat.complete(
                messages = messages,
                model = model
                )
            return response.choices[0].message.content


        elif model == 'deepseek-chat': 
            response = self.deepseek_client.chat.completions.create(
            messages = messages, 
            model = model,
            stream=False

        )
            
            return response.choices[0].message.content

        elif model == 'GigaChat-Pro':
            giga = GigaChat(
                credentials = self.gigachat_key,
                model = model,
                verify_ssl_certs=False
            )
            response = giga.chat(
                {"messages": messages}
            )
            return response.choices[0].message.content


        # await bot.send_chat_action(chat_id=message.chat.id, action = ChatAction.TYPING)
        # await asyncio.sleep(2) 

