# -*- encoding:utf-8 -*-

from lib2to3.pgen2 import token
import logging
import re
from configparser import ConfigParser
from ast import literal_eval
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, PicklePersistence
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ParseMode
from AdminTalk import ManageTalk
from Persian import Persian

GETSUP, STATAD, GETTAKID, GETTAK = range(4)
config = ConfigParser()
config.read('config.ini')

Admins = []

for i in config.get('Admins', 'admins').split(","):
    Admins.append(literal_eval(i))

persistence = PicklePersistence(filename='talkbot')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ret = "🔙 بازگشت"

def menu_admin(update, context):
    chat_id = update.message.chat_id

    if chat_id in Admins:
        keyboard = [
            [KeyboardButton(text="📩 پاسخ به پیام")]
        ]

        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="↩️ شما به صفحه اصلی بازگشتید", reply_markup=rp)

    else:
        pass

def start(update, context):
    chat_id = update.message.chat_id

    if chat_id not in Admins:
        context.bot.send_message(chat_id=chat_id, text=
        "🤖 بات پشتیبانی ورودی مهر ۱۴۰۰ پزشکی شیراز" + "\n" + "\n<b>این بات صرفا برای پشتیبانی و ارتباط با ادمین های بات اصلی طراحی شده است</b>" + "\n" + "\n<b>بات اصلی 👇:</b>" + "\n" + "@Sums1400_Bot" + "\n" + "\n\nجهت ارتباط با پشتیبانی پیام یا سوال خود را بصورت کامل و در قالب یک پیام ارسال کنید (ارسال فایل آزاد است):",
        parse_mode = ParseMode.HTML
        )

        getsup(update, context)
        return GETSUP
    
    elif chat_id in Admins:
        keyboard = [
            [KeyboardButton(text="📩 پاسخ به پیام")]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        context.bot.send_message(chat_id=chat_id, text="مقام ادمین شما شناسایی شد!", reply_markup=rp)

        statadmin(update, context)
        return STATAD

    else:
        pass

def statadmin(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "📩 پاسخ به پیام":
        keyboard = [
            [KeyboardButton(text=ret)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        context.bot.send_message(chat_id=chat_id, text="لطفا شماره کاربری کاربر مورد نظر را ارسال کنید: " , reply_markup = rp)

        gettakid(update, context)
        return GETTAKID

    else:
        pass

def gettakid(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    
    if update.message.from_user.is_bot:
        pass
    
    else:
        if text == ret:
            menu_admin(update, context)
            return STATAD

        elif text == "📩 پاسخ به پیام":
            pass

        else:
            reg = re.compile('^[0-9]+$')
            cr = reg.match(str(text))

            if cr:
                global chatsend
                chatsend = Persian().convert(text=text)

                keyboard = [
                    [KeyboardButton(text=ret)]
                ]
                rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

                context.bot.send_message(chat_id=chat_id, text="لطفا پیام ([document, video, photo, voice, text])مورد نظر را برای ارسال به کاربر ارسال کنید:" , reply_markup = rp)

                gettak(update, context)
                return GETTAK
            
            else:
                context.bot.send_message(chat_id=chat_id, text="⚠️ فرمت نامعتبر")

def gettak(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if update.message.from_user.is_bot:
        pass

    else:
        if text == ret:
            menu_admin(update, context)
            return STATAD
        
        elif text == chatsend:
            pass

        elif text == "📩 ارسال پیام تکی":
            pass

        else:
            updatee = update.message
            t = updatee["text"]
            vi = updatee["video"]
            vo = updatee["voice"]
            p = updatee["photo"]
            d = updatee["document"]

            if t != None:
                mid = updatee["message_id"]
                if ManageTalk().send_message_tak(from_id=chat_id, mid=mid, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
                    for i in Admins:
                        try:
                            context.bot.send_message(chat_id=i, text=f"جواب شماره کاربری {str(chatsend)} توسط {chat_id} داده شد!")

                        except:
                            continue

                    menu_admin(update, context)
                    return STATAD
                
                else:
                    context.bot.send_message(chat_id=chat_id, text="❌ خطا در ارسال پیام")
                    menu_admin(update, context)
                    return STATAD

            elif vi != None:
                file_id = update.message.video.file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""

                if ManageTalk().send_video_tak(video=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
                    for i in Admins:
                        try:
                            context.bot.send_message(chat_id=i, text=f"جواب شماره کاربری {str(chatsend)} توسط {chat_id} داده شد!")

                        except:
                            continue
                    menu_admin(update, context)
                    return STATAD
                
                else:
                    context.bot.send_message(chat_id=chat_id, text="❌ خطا در ارسال پیام")
                    menu_admin(update, context)
                    return STATAD

            elif vo != None:
                file_id = update.message.voice.file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""

                if ManageTalk().send_voice_tak(voice=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
                    for i in Admins:
                        try:
                            context.bot.send_message(chat_id=i, text=f"جواب شماره کاربری {str(chatsend)} توسط {chat_id} داده شد!")

                        except:
                            continue
                    menu_admin(update, context)
                    return STATAD
                
                else:
                    context.bot.send_message(chat_id=chat_id, text="❌ خطا در ارسال پیام")
                    menu_admin(update, context)
                    return STATAD

            elif p != None and p != []:
                file_id = update.message.photo[0].file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""

                if ManageTalk().send_photo_tak(photo=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
                    for i in Admins:
                        try:
                            context.bot.send_message(chat_id=i, text=f"جواب شماره کاربری {str(chatsend)} توسط {chat_id} داده شد!")

                        except:
                            continue
                    menu_admin(update, context)
                    return STATAD
                
                else:
                    context.bot.send_message(chat_id=chat_id, text="❌ خطا در ارسال پیام")
                    menu_admin(update, context)
                    return STATAD

            elif d != None:
                file_id = update.message.document.file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""

                if ManageTalk().send_document_tak(document=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
                    for i in Admins:
                        try:
                            context.bot.send_message(chat_id=i, text=f"جواب شماره کاربری {str(chatsend)} توسط {chat_id} داده شد!")

                        except:
                            continue
                    menu_admin(update, context)
                    return STATAD
                
                else:
                    context.bot.send_message(chat_id=chat_id, text="❌ خطا در ارسال پیام")
                    menu_admin(update, context)
                    return STATAD
            
            else:
                context.bot.send_message(chat_id=chat_id, text="⚠️ فرمت فایل نامعتبر است")
                menu_admin(update, context)
                return STATAD

def getsup(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if update.message.from_user.is_bot:
        pass

    else:
        if text == "🤖 بات پشتیبانی ورودی مهر ۱۴۰۰ پزشکی شیراز" + "\n" + "\n<b>این بات صرفا برای پشتیبانی و ارتباط با ادمین های بات اصلی طراحی شده است</b>" + "\n" + "\n<b>بات اصلی 👇:</b>" + "\n" + "@Sums1400_Bot" + "\n" + "\n\nجهت ارتباط با پشتیبانی پیام یا سوال خود را بصورت کامل و در قالب یک پیام ارسال کنید (ارسال فایل آزاد است):":
            pass
        
        elif text == "پیام شما با موفقیت برای ادمین های بات ارسال شد ✅":
            pass

        elif text == "/start":
            pass

        else:
            for i in Admins:
                try:
                    context.bot.send_message(chat_id=i, text='پیام جدید از شماره کاربری `{}` 👇:'.format(str(chat_id)), parse_mode=ParseMode.MARKDOWN_V2)
                    context.bot.forward_message(chat_id=i, from_chat_id=chat_id, message_id=update.message.message_id)
                
                except:
                    continue
            
            context.bot.send_message(chat_id=chat_id, text="پیام شما با موفقیت برای ادمین های بات ارسال شد ✅")

def cancel(update, context):
    pass
    
def main():
    token = config.get('TOKENS', 'support_bot_token')
    updater = Updater(token=token, persistence=persistence)
    
    dispatcher = updater.dispatcher

    conv_handl = ConversationHandler (
        entry_points = [CommandHandler('start', start)],

        states= {
            GETSUP : [MessageHandler(Filters.all, getsup)],
            STATAD : [MessageHandler(Filters.text, statadmin)],
            GETTAKID : [MessageHandler(Filters.text, gettakid)],
            GETTAK : [MessageHandler(Filters.all, gettak)],
        },

        fallbacks=[CommandHandler('halalalaylalay', cancel)],

        allow_reentry=True,

        persistent=True,

        name="talkhandl"
    )

    dispatcher.add_handler(conv_handl)


    updater.start_polling()
    updater.idle()

if 4 == 4:
    main()