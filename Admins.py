# -*- encoding:utf-8 -*-

import sqlite3
import re
from configparser import ConfigParser
from time import sleep
from telegram import Bot, ParseMode, TelegramError
from ast import literal_eval

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

config = ConfigParser()
config.read('config.ini')

TOKEN = config.get('TOKENS', 'main_bot_token')

class Manage():
    def __init__(self):
        pass

    def count_member(self):
        cursor.execute('SELECT COUNT(*) FROM Members')
        c = cursor.fetchall()
        return c[0][0]

    def get_list(self):
        cursor.execute('SELECT * FROM Members')
        rows = cursor.fetchall()

        return rows
    
    def send_message(self, from_id, mid):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).copy_message(chat_id=chat_id, from_chat_id=from_id, message_id=mid, parse_mode=ParseMode.MARKDOWN_V2)
                sleep(1)

            except:
                continue

    def send_video(self, video, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_video(chat_id=chat_id, video=video, caption=caption)
                sleep(1)
            
            except:
                continue

    def send_document(self, document, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_document(chat_id=chat_id, document=document, caption=caption)
                sleep(1)
            
            except:
                continue

    def send_photo(self, photo, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_photo(chat_id=chat_id, photo=photo, caption=caption)
                sleep(1)
            
            except:
                continue

    def send_voice(self, voice, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_voice(chat_id=chat_id, voice=voice, caption=caption)
                sleep(1)
            
            except:
                continue
    
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