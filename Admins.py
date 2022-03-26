# -*- coding:utf-8 -*-

import sqlite3
import re
from time import sleep
from telegram import Bot, ParseMode, TelegramError
from ast import literal_eval
from hashlib import md5
import config

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

TOKEN = config.MAIN_BOT_TOKEN

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
    
    def get_admins_login(self, username, password):
        password = md5(password.encode()).hexdigest()
        cursor.execute('SELECT * FROM Admins WHERE User_name=? and Password=?', (username, password))
        rows = cursor.fetchall()
        
        if rows == []:
            return "False"
        
        else:
            return rows[0][2]

    def block_unblock(self, user_id):
        reg = re.compile('^[0-9]+$')
        cr = reg.match(str(user_id))

        if cr:
            cursor.execute('SELECT * FROM Blocked WHERE Chat_id=?', (literal_eval(user_id),))
            rows = cursor.fetchall()

            if rows == []:
                cursor.execute('insert into Blocked(Chat_id) values(?)', (literal_eval(user_id),))
                conn.commit()

                return True

            else:
                cursor.execute("DELETE from Blocked where Chat_id=?", (literal_eval(user_id),))
                conn.commit()

                return False
            
        else:
            return "Error"

    def get_block(self):
        Blocked = []

        cursor.execute('SELECT Chat_id from Blocked')
        users = cursor.fetchall()

        for i in range(len(users)):
            Blocked.append(users[i][0])
        
        return Blocked
    
    def get_block_info(self):
        Blocked = self.get_block()
        
        info = []

        for i in Blocked:
            try:
                cursor.execute('SELECT * FROM Members WHERE User_id=?', (i,))
                rows = cursor.fetchall()
                info.append(rows[0])
    
            except IndexError:
                info.append(("User not joined","User not joined","User not joined",i,i,"User not joined"))
        
        
        return info
    
    def send_message(self, from_id, mid):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).copy_message(chat_id=chat_id, from_chat_id=from_id, message_id=mid, parse_mode=ParseMode.MARKDOWN_V2)
                sleep(2)

            except:
                continue

    def send_text_message(self, text):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2)
                sleep(2)

            except:
                continue

    def send_video(self, video, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_video(chat_id=chat_id, video=video, caption=caption)
                sleep(2)
            
            except:
                continue

    def send_document(self, document, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_document(chat_id=chat_id, document=document, caption=caption)
                sleep(2)
            
            except:
                continue

    def send_photo(self, photo, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_photo(chat_id=chat_id, photo=photo, caption=caption)
                sleep(2)
            
            except:
                continue

    def send_voice(self, voice, caption):
        cursor.execute('SELECT User_id from Members')
        users = cursor.fetchall()

        for i in range(len(users)):
            try:
                chat_id = literal_eval(users[i][0])
                Bot(token=TOKEN).send_voice(chat_id=chat_id, voice=voice, caption=caption)
                sleep(2)
            
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

class Prefix():
    def __init__(self):
        pass

    def prefixt2(self, query):

        cursor.execute('SELECT * FROM Prefix')
        rows = cursor.fetchall()

        p = ["ta", "es", "hea", "cht2", "chat2", "att2", "phya", "za2", "an1", "en", "tgh", "com", "khl", "ada2", "jam"]

        all_pre = []
        pre_tarif = []
        pre_ntarif = []
        pre_ta = []
        pre_es = []
        pre_hea = []
        pre_cht2 = []
        pre_chat2 = []
        pre_att2 = []
        pre_phya = []
        pre_za2 = []
        pre_an1 = []
        pre_en = []
        pre_tgh = []
        pre_com = []
        pre_khl = []
        pre_ada2 = []
        pre_jam = []

        for i in rows:
            all_pre.append(i[0])

        for i in p:
            for m in all_pre:
                if i in m[:6]:
                    pre_tarif.append(m)
        
        for i in all_pre:
            if i in pre_tarif:
                pass

            else:
                pre_ntarif.append(i)

        for i in pre_tarif:
            if "ta" in i:
                pre_ta.append(i)
            
            elif "es" in i:
                pre_es.append(i)
            
            elif "hea" in i:
                pre_hea.append(i)
            
            elif "cht2" in i:
                pre_cht2.append(i)
            
            elif "chat2" in i:
                pre_chat2.append(i)
            
            elif "att2" in i:
                pre_att2.append(i)
            
            elif "phya" in i:
                pre_phya.append(i)
            
            elif "za2" in i:
                pre_za2.append(i)
            
            elif "an1" in i:
                pre_an1.append(i)
            
            elif "en" in i:
                pre_en.append(i)
            
            elif "tgh" in i:
                pre_tgh.append(i)
            
            elif "com" in i:
                pre_com.append(i)
            
            elif "khl" in i:
                pre_khl.append(i)
            
            elif "ada2" in i:
                pre_ada2.append(i)
            
            elif "jam" in i:
                pre_jam.append(i)
            
            else:
                pass
        
        if query == "ta":
            res = []
            for i in pre_ta:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "es":
            res = []
            for i in pre_es:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res

        elif query == "hea":
            res = []
            for i in pre_hea:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "cht2":
            res = []
            for i in pre_cht2:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "chat2":
            res = []
            for i in pre_chat2:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "att2":
            res = []
            for i in pre_att2:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "phya":
            res = []
            for i in pre_phya:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "za2":
            res = []
            for i in pre_za2:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "an1":
            res = []
            for i in pre_an1:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "en":
            res = []
            for i in pre_en:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "tgh":
            res = []
            for i in pre_tgh:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "com":
            res = []
            for i in pre_com:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "khl":
            res = []
            for i in pre_khl:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "ada2":
            res = []
            for i in pre_ada2:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "jam":
            res = []
            for i in pre_jam:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        elif query == "other":
            res = []
            for i in pre_ntarif:
                cursor.execute('SELECT * FROM Prefix WHERE Prefix=?', (i,))
                rows = cursor.fetchall()
                res.append(rows[0])
            
            return res
        
        else:
            return False