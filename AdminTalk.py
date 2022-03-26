# -*- coding:utf-8 -*-

from telegram import Bot, ParseMode, TelegramError
from ast import literal_eval
import config

TOKEN = config.SUPPORT_BOT_TOKEN

class ManageTalk():
    def __init__(self):
        pass
    
    def send_message_tak(self, from_id, mid, chat_id):
        try:
            chat_id = literal_eval(chat_id)
            Bot(token=TOKEN).copy_message(chat_id=chat_id, from_chat_id=from_id, message_id=mid, parse_mode=ParseMode.MARKDOWN_V2)

            return True
        
        except:
            return False

    def send_video_tak(self, video, caption, chat_id):
        try:
            chat_id = literal_eval(chat_id)
            Bot(token=TOKEN).send_video(chat_id=chat_id, video=video, caption=caption)

            return True
        
        except:
            return False

    def send_document_tak(self, document, caption, chat_id):
        try:
            chat_id = literal_eval(chat_id)
            Bot(token=TOKEN).send_document(chat_id=chat_id, document=document, caption=caption)

            return True
        
        except:
            return False

    def send_photo_tak(self, photo, caption, chat_id):
        try:
            chat_id = literal_eval(chat_id)
            Bot(token=TOKEN).send_photo(chat_id=chat_id, photo=photo, caption=caption)

            return True
        
        except:
            return False

    def send_voice_tak(self, voice, caption, chat_id):
        try:
            chat_id = literal_eval(chat_id)
            Bot(token=TOKEN).send_voice(chat_id=chat_id, voice=voice, caption=caption)

            return True
        
        except:
            return False