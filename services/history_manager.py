import json
import logging
import boto3
import os

from dotenv import load_dotenv
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_s3_client():
    load_dotenv()

    yandex_id = os.getenv('YANDEX_ID')
    yandex_key = os.getenv('YANDEX_KEY')
    endpoint = os.getenv('ENDPOINT')
    
    session = boto3.Session(
        aws_access_key_id=yandex_id,
        aws_secret_access_key=yandex_key,
    )
    return session.client(service_name='s3', endpoint_url=endpoint)

class HistoryManager:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = get_s3_client()


    async def get_history(self, chat_id: int) -> List[Dict]:
        try:
            obj = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"{chat_id}.json",
            )
            return json.loads(obj["Body"].read())
        except Exception as e:
            logger.warning(f"История для {chat_id} не найдена: {e}")
            return []

    async def save_history(self, chat_id: int, history: List[Dict]) -> None:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f"{chat_id}.json",
                Body=json.dumps(history),
            )
        except Exception as e:
            logger.error(f"Ошибка сохранения истории {chat_id}: {e}")

    async def add_message(self, chat_id: int, role: str, content: str, max_messages: int = 10) -> List[Dict]:
        history = await self.get_history(chat_id)
        history.append({"role": role, "content": content})
        
        if len(history) > max_messages * 2:
            history = history[-(max_messages * 2):]
        
        await self.save_history(chat_id, history)
        return history

    async def clear_history(self, chat_id: int) -> None:
        await self.save_history(chat_id, [])
        logger.info(f"История для {chat_id} очищена")