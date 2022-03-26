# -*- coding:utf-8 -*-

import sqlite3
import time
import json
import logging
import re
from ast import literal_eval
from copy import copy
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, run_async
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from requests import get as getrequests
from Admins import Manage
from Persian import Persian
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

con = sqlite3.connect("bot.db", check_same_thread=False)
c = con.cursor()

STAT, DOROST1, CHBIO, CHOT, CHSOTA, CHSOTN, CHSBIOA, CHSBION, CHSP, CHSR, CHSPH, CHSPE, CHSE1, CHSDA, CHSVBION, CHSVBIOA, CHSVOTN, CHSVOTA, CHSVP, CHSVR, CHSVPH, GETTERMBANK, SENDBANKT1, SENDBANKT2 = range(24)
STATAD, GETSAR, GETTAK, GETTAKID, GETBAN, GETPRE, GETPREFILE, GETPREDEL, STATBLOCK, GETTERMCATEG = range(1000,1010)

Admins = config.ADMINS

#Change Before Config
SITE_ADDRESS = config.SITE_ADDRESS
SEC_TOKEN = config.SEC_TOKEN

#Change Before Config
BOT_ID = "@Sums1400_Bot"
BOT_ID2 = BOT_ID.replace("@", "")

ret = "🔙 بازگشت"
ret_menu = "🔙 بازگشت به منوی اصلی"

MAX_USAGE = config.MAX_USAGE

keyboard_doros_term1 = [
    [KeyboardButton(text="علوم تشریح 💀")],
    [KeyboardButton(text="بیوشیمی 🧪")],
    [KeyboardButton(text="فیزیولوژی 🔎")],
    [KeyboardButton(text="روانشناسی 🧠")],
    [KeyboardButton(text="فیزیک پزشکی 😭")],
    [KeyboardButton(text="فارسی 🇮🇷")],
    [KeyboardButton(text="زبان عمومی " + "1️⃣")],
    [KeyboardButton(text="دانش خانواده 👨‍👩‍👧‍👦")],
    [KeyboardButton(text=ret)]
]

keyboard_doros_term2 = [
    [KeyboardButton(text="دستگاه قلب 🫀")],
    [KeyboardButton(text="دستگاه تنفس 🫁")],
    [KeyboardButton(text="دستگاه غدد 🌋")],
    [KeyboardButton(text="بیوشیمی دیسیپلین 🧪")],
    [KeyboardButton(text="علوم تشریح عملی 💀")],
    [KeyboardButton(text="فیزیولوژی عملی 🔎")],
    [KeyboardButton(text="تغذیه 🍫")],
    [KeyboardButton(text="کامپیوتر 💻")],
    [KeyboardButton(text="زبان عمومی " + "2️⃣")],
    [KeyboardButton(text="اندیشه اسلامی 📿")],
    [KeyboardButton(text="انقلاب اسلامی 🕋")],
    [KeyboardButton(text="جامعه شناسی سلامت 👥")],
    [KeyboardButton(text="خلاقیت و کارآفرینی 💼")],
    [KeyboardButton(text=ret)]
]

keyboard_send = [
    [KeyboardButton(text="کلاس ضبطی / فایل های ویدئویی 🎥")],
    [KeyboardButton(text="جزوه / منابع 📔")],
    [KeyboardButton(text="امتحان ۱۴۰۰ 📕")],
    [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
]

keyboard_select_term = [
    [KeyboardButton(text="ترم 1️⃣")],
    [KeyboardButton(text="ترم 2️⃣")],
    [KeyboardButton(text=ret)]
]

def main_menu(update, context):
    chat_id = update.message.chat_id

    keyboard = [
        [KeyboardButton(text="ترم 1️⃣")],
        [KeyboardButton(text="ترم 2️⃣")],
        [KeyboardButton(text="🏦 بانک سوال")],
        [KeyboardButton(text="📖 نواریون")],
        [KeyboardButton(text="📎 برنامه دروس و امتحانات")],
        [KeyboardButton(text="👤 پنل کاربری"), KeyboardButton(text="👨‍💻 پشتیبانی")],
    ]

    keyboard_adm = [
        [KeyboardButton(text="😎 پنل مدیریت")],
        [KeyboardButton(text="ترم 1️⃣")],
        [KeyboardButton(text="ترم 2️⃣")],
        [KeyboardButton(text="🏦 بانک سوال")],
        [KeyboardButton(text="📖 نواریون")],
        [KeyboardButton(text="📎 برنامه دروس و امتحانات")],
        [KeyboardButton(text="👤 پنل کاربری"), KeyboardButton(text="👨‍💻 پشتیبانی")], 
    ]

    c.execute('SELECT * FROM Members WHERE Chat_id=?', (str(chat_id),))
    rows = c.fetchall()

    if rows == []:
        chat_id2 = str(chat_id)
        first_name = str(update.message.from_user.first_name)
        last_name = str(update.message.from_user.last_name)
        user_name = str(update.message.from_user.username)
        user_id = str(update.message.from_user.id)

        if user_name == "None":
            user_name = "Empty"

        else:
            user_name = "@" + user_name

        if first_name == "None":
            first_name = "Empty"

        else:
            first_name = first_name

        if last_name == "None":
            last_name = "Empty"

        else:
            last_name = last_name

        date = str(update.message.date)
        c.execute('insert into Members(Name,Last_name,User_name,Chat_id, User_id, Time_joined) values(?, ?, ?, ?, ?, ?)', (first_name, last_name, user_name, chat_id2, user_id ,date))
        con.commit()

    else:
        pass
    
    if chat_id in Admins:
        context.bot.send_message(chat_id=chat_id, text="مقام ادمین شما شناسایی شد!")
        context.bot.send_message(chat_id=chat_id, text="درود <a href='tg://user?id={}'>{}</a> 👋".format(chat_id, update.message.from_user.first_name) + "\n<b>به ربات پزشکی مهر ۱۴۰۰ شیراز</b> خوش اومدی!" + "\nلطفا از منوی زیر انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard_adm, resize_keyboard=True), parse_mode=ParseMode.HTML)    
    
    else:
        context.bot.send_message(chat_id=chat_id, text="درود <a href='tg://user?id={}'>{}</a> 👋".format(chat_id, update.message.from_user.first_name) + "\n<b>به ربات پزشکی مهر ۱۴۰۰ شیراز</b> خوش اومدی!" + "\nلطفا از منوی زیر انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True), parse_mode=ParseMode.HTML)

def getinfofromjson():
    with open("files.json") as jj:
        j = json.load(jj, strict=False)
    
    return j

def menu(update, context):
    chat_id = update.message.chat_id
    Blocked = Manage().get_block()
  
    keyboard = [
        [KeyboardButton(text="ترم 1️⃣")],
        [KeyboardButton(text="ترم 2️⃣")],
        [KeyboardButton(text="🏦 بانک سوال")],
        [KeyboardButton(text="📖 نواریون")],
        [KeyboardButton(text="📎 برنامه دروس و امتحانات")],
        [KeyboardButton(text="👤 پنل کاربری"), KeyboardButton(text="👨‍💻 پشتیبانی")],
    ]

    keyboard_adm = [
        [KeyboardButton(text="😎 پنل مدیریت")],
        [KeyboardButton(text="ترم 1️⃣")],
        [KeyboardButton(text="ترم 2️⃣")],
        [KeyboardButton(text="🏦 بانک سوال")],
        [KeyboardButton(text="📖 نواریون")],
        [KeyboardButton(text="📎 برنامه دروس و امتحانات")],
        [KeyboardButton(text="👤 پنل کاربری"), KeyboardButton(text="👨‍💻 پشتیبانی")], 
    ]

    if chat_id not in Blocked:
        if chat_id in Admins:
            markup = ReplyKeyboardMarkup(keyboard_adm, resize_keyboard=True ,one_time_keyboard=False)
        
        else:
            markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True ,one_time_keyboard=False)

        context.bot.send_message(chat_id=chat_id, text="↩️ شما به منوی اصلی بازگشتید", reply_markup=markup)
    
    else:
        context.bot.send_message(chat_id=chat_id, text="لطفا در سریع ترین زمان ممکن دکمه خروج را فشار دهید", reply_markup=ReplyKeyboardRemove())

def menu_admin(update, context):
    chat_id = update.message.chat_id

    if chat_id in Admins:
        keyboard = [
            [KeyboardButton(text="📊 آمار کاربران")],
            [KeyboardButton(text="👤 مشاهده لیست کابران")],
            [KeyboardButton(text="📩 ارسال پیام سراسری")],
            [KeyboardButton(text="📩 ارسال پیام تکی")],
            [KeyboardButton(text="🚫 بن و آنبن کاربران")],
            [KeyboardButton(text="➕ اضافه کردن Prefix")],
            [KeyboardButton(text="➖ حذف کردن Prefix")],
            [KeyboardButton(text="🗄 دسته بندی Prefix")],
            [KeyboardButton(text=ret_menu)]
        ]

        markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="↩️ شما به پنل مدیریت بازگشتید", reply_markup=markup)

    else:
        pass

def check_channel(update, context):
    chat_id = update.message.chat_id
    #Change Before Config
    channel_id  = config.CHANNEL

    keyboard = [
        [InlineKeyboardButton(text="برای عضویت کلیک کنید", url="https://telegram.me/" + channel_id.replace("@", ""))]
    ]

    context.bot.send_message(chat_id=chat_id, text="شما امکان استفاده از بات را ندارید", reply_markup=ReplyKeyboardRemove())
    context.bot.send_message(chat_id=chat_id, text="شما هنوز در کانال آرشیو 1400 عضو نشده اید، ابتدا در کانال زیر عضو شده و سپس دوباره /start را وارد کنید", reply_markup=InlineKeyboardMarkup(keyboard))

def start(update, context):
    chat_id = update.message.chat_id
    channel = config.CHANNEL
    status = []
    ftype_l = ["document", "video", "photo", "voice"]

    #Change Before Config
    chat = context.bot.get_chat_member(chat_id=channel, user_id=update.message.from_user.id)
    status.append(chat.status)
    Blocked = Manage().get_block()

    if "left" not in status and 'kicked' not in status and 'restricted' not in status and 'banned' not in status and chat_id not in Blocked:

        if len(context.args) == 0:
            main_menu(update, context)
            return STAT

        else:
            c.execute('SELECT * FROM Prefix WHERE Prefix=?', (context.args[0],))
            rows = c.fetchall()

            if rows == []:
                main_menu(update, context)
                return STAT

            else:
                ftype = rows[0][1]
                if ftype in ftype_l:
                    file_id = rows[0][2]
                    caption = rows[0][3]

                    if ftype == "video":
                        context.bot.send_video(chat_id=chat_id, video=file_id, caption=caption)

                    elif ftype == "document":
                        context.bot.send_document(chat_id=chat_id, document=file_id, caption=caption)

                    elif ftype == "photo":
                        context.bot.send_photo(chat_id=chat_id, photo=file_id, caption=caption)

                    elif ftype == "voice":
                        context.bot.send_voice(chat_id=chat_id, voice=file_id, caption=caption)
                    
                    else:
                        pass

                else:
                    main_menu(update, context)
                    return STAT
    
    elif chat_id in Blocked:
        context.bot.send_message(chat_id=chat_id, text="لطفا در سریع ترین زمان ممکن دکمه خروج را فشار دهید", reply_markup=ReplyKeyboardRemove())

    else:
        check_channel(update, context)

def stat(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    Blocked = Manage().get_block()

    count = context.user_data.get("usageCount", 0)
    restrict_since = context.user_data.get("restrictSince", 0)
    last_message = context.user_data.get("lastMessage", 0)
    
    if chat_id not in Blocked and not restrict_since:
        if text == "ترم 1️⃣":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
            dt1(update, context)
            return DOROST1
        
        elif text == "ترم 2️⃣":
            if count == MAX_USAGE:
                context.user_data["restrictSince"] = time.time()
                update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_message(chat_id=chat_id, text="فایل های مربوط به ترم ۲ بعد از کامل شدن در بات قرار می گیرد")
        
        elif text == "🏦 بانک سوال":
            keyboard = [
                [KeyboardButton(text="ترم 1️⃣")],
                [KeyboardButton(text="ترم 2️⃣")],
                [KeyboardButton(text=ret)]
            ]

            rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

            context.bot.send_message(chat_id=chat_id, text="لطفا ترم مورد نظر را از منوی زیر انتخاب کنید: ", reply_markup=rp)

            gettermbank(update, context)
            return GETTERMBANK

        elif text == "📖 نواریون":
            jn = getinfofromjson()["Navariyoon"]
            jn_e = getinfofromjson()["Navariyoon_Enable"]

            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")

            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                if jn_e == "True":
                    for i in jn["file"]:
                        context.bot.send_document(chat_id=chat_id, document=i, caption=jn["caption"])
                
                else:
                    context.bot.send_message(chat_id=chat_id, text="نواریون مهر ۱۴۰۰" + "\n" + "Coming Soon...!")
        
        elif text == "📎 برنامه دروس و امتحانات":
            jp = getinfofromjson()["Program"]

            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()
                
                context.bot.send_document(chat_id=chat_id, document=jp["Emtehan"], caption="📄 برنامه امتحانات ترم جدید" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jp["Koli"], caption="📄 برنامه کلی دروس ترم جدید" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jp["Edqam"], caption="📄 برنامه دروس ادغام ترم جدید" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jp["qEdqam"], caption="📄 برنامه دروس غیر ادغام ترم جدید" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jp["Ekhtiari"], caption="📄 برنامه دروس اختیاری ترم جدید" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "👤 پنل کاربری":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()
                
                if chat_id  not in Admins:
                    context.bot.send_message(chat_id=chat_id, text='👤 شماره کاربری: {} \n👤 نوع کاربر: {}'.format(str(update.message.from_user.id), "کاربر عادی") + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                
                else:
                    context.bot.send_message(chat_id=chat_id, text='👤 شماره کاربری: {} \n👤 نوع کاربر: {}'.format(str(update.message.from_user.id), "ادمین :))))))")+ "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "👨‍💻 پشتیبانی":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
    
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_message(chat_id=chat_id, text="در صورتی که سوال انتقاد و یا پیشنهادی برای بات دارید از طریق بات زیر می توانید با ادمین های ما ارتباط برقرار کنید 👇: \n" + "@Sums1400Talk_Bot")

        
        elif text == "😎 پنل مدیریت":
            if chat_id in Admins:
                keyboard = [
                    [KeyboardButton(text="📊 آمار کاربران")],
                    [KeyboardButton(text="👤 مشاهده لیست کابران")],
                    [KeyboardButton(text="📩 ارسال پیام سراسری")],
                    [KeyboardButton(text="📩 ارسال پیام تکی")],
                    [KeyboardButton(text="🚫 بن و آنبن کاربران")],
                    [KeyboardButton(text="➕ اضافه کردن Prefix")],
                    [KeyboardButton(text="➖ حذف کردن Prefix")],
                    [KeyboardButton(text="🗄 دسته بندی Prefix")],
                    [KeyboardButton(text=ret_menu)],
                ]

                markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
                context.bot.send_message(chat_id=chat_id, text=" پنل مدیریت از طریق سایت زیر نیز در دسترس میباشد: " + "\n" + "https://sumsmd1400.ir/bot"  + "\n\n" + "لطفا یک گزینه را انتخاب کنید:", reply_markup=markup)
                statadmin(update, context)
                return STATAD

            else:
                context.bot.send_message(chat_id=chat_id, text="بچه برو دنبال بازیت" + "\n" + "برا ما هکر شده")

        else:
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
    
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

    elif restrict_since:
        if (time.time() - restrict_since) >= 300: # 5 minutes
            del context.user_data["restrictSince"]
            del context.user_data["usageCount"]
            update.effective_message.reply_text("⚠️ محدودیت شما به اتمام رسید")
        else:
            update.effective_message.reply_text("⚠️ زمان محدودیت شما به اتمام نرسیده است" + "\n" + f"زمان باقی مانده به ثانیه: {str(round(300 - (time.time() - restrict_since)))}")

    else:
        pass

def statadmin(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "📊 آمار کاربران":
        cm = Manage().count_member()
        context.bot.send_message(chat_id=chat_id, text="📊 تعداد کل کاربران: " + "\n" + str(cm) + "\n" + "📊 تعداد کاربران فعال: "+ "\n" + str(cm))
    
    elif text == "👤 مشاهده لیست کابران":
        context.bot.send_message(chat_id=chat_id, text=f'[برای مشاهده لیست کاربران کلیک کنید]({SITE_ADDRESS}/v1/{SEC_TOKEN}/members)', parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

    elif text == "📩 ارسال پیام سراسری":
        keyboard = [
            [KeyboardButton(text=ret)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        context.bot.send_message(chat_id=chat_id, text="لطفا پیام ([document, video, photo, voice, text]) را برای ارسال سراسری به کاربران بات ارسال کنید:" + "\n" + "\nجان موحدی حواستون باشه پیامی که اینجا میفرستید برای همه اعضا میره هیچ جوره هم نمیشه جلوشو گرفت 🙃", reply_markup = rp)
        getsar(update, context)
        return GETSAR
    
    elif text == "📩 ارسال پیام تکی":
        keyboard = [
            [KeyboardButton(text=ret)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        context.bot.send_message(chat_id=chat_id, text="لطفا شماره کاربری کاربر مورد نظر را ارسال کنید: " , reply_markup = rp)

        gettakid(update, context)
        return GETTAKID

    elif text == "🚫 بن و آنبن کاربران":
        keyboard = [
            [KeyboardButton(text=ret)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        Blocked = Manage().get_block()

        context.bot.send_message(chat_id=chat_id, text="🚫 لیست افراد بن شده:" + "\n" + str(Blocked) + "\n" + "برای بن یا آنبن شماره کاربری کاربر نظر را ارسال کنید:", reply_markup = rp)

        getban(update, context)
        return GETBAN

    elif text == "➕ اضافه کردن Prefix":
        keyboard = [
            [KeyboardButton(text=ret)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        context.bot.send_message(chat_id=chat_id, text="لطفا Prefix مورد نظر را ارسال کنید:", reply_markup=rp)

        getpre(update, text)
        return GETPRE

    elif text == "➖ حذف کردن Prefix":
        keyboard = [
            [KeyboardButton(text=ret)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        prefixlist = []

        c.execute('SELECT Prefix from Prefix')
        res = c.fetchall()


        for i in range(len(res)):
            prefixlist.append(res[i][0])

        context.bot.send_message(chat_id=chat_id, text="🔍 لیست Prefix ها: " + "\n" + str(prefixlist) + "\n" +"\nلطفا Prefix مورد نظر را ارسال کنید:", reply_markup=rp)

        getpredel(update, context)
        return GETPREDEL

    elif text == "🗄 دسته بندی Prefix":
        keyboard = [
            [KeyboardButton(text="ترم 2️⃣")],
            [KeyboardButton(text=ret)]
        ]
        
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        context.bot.send_message(chat_id=chat_id,  text="لطفا ترم مورد نظر را انتخاب کنید:",  reply_markup=rp)
        gettermcateg(update, context)
        return GETTERMCATEG

    elif text == ret_menu:
        menu(update, context)
        return STAT
    
    else:
        pass

def getpredel(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    prefixlist = []

    c.execute('SELECT Prefix from Prefix')
    res = c.fetchall()


    for i in range(len(res)):
        prefixlist.append(res[i][0])

    if text == ret:
        menu_admin(update, context)
        return STATAD
    
    elif text == "➖ حذف کردن Prefix":
        pass

    elif text == "🔍 لیست Prefix ها: " + "\n" + str(prefixlist) + "\n" +"\nلطفا Prefix مورد نظر را ارسال کنید:":
        pass

    elif text == "⚠️ فرمت نامعتبر":
        pass

    elif text == "⚠️ پیدا نشد":
        pass

    else:
        text = Persian().convert(text=str(text))
        reg = re.compile('^[a-zA-Z0-9]+$')
        cr = reg.match(str(text))

        if not cr:
            context.bot.send_message(chat_id=chat_id, text="⚠️ فرمت نامعتبر")

        else:
            pref = text.lower()

            c.execute('SELECT * FROM Prefix WHERE Prefix=?', (pref,))
            rows = c.fetchall()

            if rows == []:
                context.bot.send_message(chat_id=chat_id, text="⚠️ پیدا نشد")
            
            else:
                c.execute("DELETE from Prefix where Prefix=?", (pref,))
                con.commit()

                context.bot.send_message(chat_id=chat_id, text="✅ Prefix با موفقیت حذف شد")

                menu_admin(update, context)
                return STATAD      

def gettermcateg(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "ترم 2️⃣":
        context.bot.send_message(chat_id=chat_id, text=f"ترم انتخابی: {text}\n\n" + f'[برای مشاهده کلیک کنید]({SITE_ADDRESS}/v1/{SEC_TOKEN}/prefixt2)', parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    
    elif text == ret:
        menu_admin(update, context)
        return STATAD
    
    else:
        pass

def getpre(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == ret:
        menu_admin(update, context)
        return STATAD

    elif text == "لطفا Prefix مورد نظر را ارسال کنید:":
        pass

    elif text == "➕ اضافه کردن Prefix":
        pass

    elif text == "⚠️ فقط حروف انگلیسی و اعداد مجاز هستند":
        pass
    

    elif text == "⚠️ ارسالی قبلا ثبت شده است Prefix" + "\n" + "لطفا Prefix دیگری را ارسال کنید:":
        pass

    elif text == "✅ با موفقیت ثبت شد Prefix" + "\n" + "لطفا فایلی را که میخواهید Prefix روی آن قرار بگیرد را ارسال کنید:":
        pass

    else:
        reg = re.compile('^[a-zA-Z0-9]+$')
        cr = reg.match(str(text))

        if not cr:
            context.bot.send_message(chat_id=chat_id, text="⚠️ فقط حروف انگلیسی و اعداد مجاز هستند")
        
        else:
            c.execute('SELECT * FROM Prefix WHERE Prefix=?', (Persian().convert(text=text.lower()),))
            rows = c.fetchall()

            if rows == []:
                keyboard = [
                    [KeyboardButton(text=ret)]
                ]
                rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

                global pre
                pre = Persian().convert(text=text)
                context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ثبت شد Prefix" + "\n" + "لطفا فایلی را که میخواهید Prefix روی آن قرار بگیرد را ارسال کنید:", reply_markup=rp)

                getprefile(update, context)
                return GETPREFILE
            
            else:
                context.bot.send_message(chat_id=chat_id, text="⚠️ ارسالی قبلا ثبت شده است Prefix" + "\n" + "لطفا Prefix دیگری را ارسال کنید:")

def getprefile(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if text == ret:
        menu_admin(update, context)
        return STATAD

    elif text == "لطفا Prefix مورد نظر را ارسال کنید:":
        pass

    elif text == "➕ اضافه کردن Prefix":
        pass

    elif text == "⚠️ فقط حروف انگلیسی و اعداد مجاز هستند":
        pass
    

    elif text == "⚠️ ارسالی قبلا ثبت شده است Prefix" + "\n" + "لطفا Prefix دیگری را ارسال کنید:":
        pass

    elif text == "✅ با موفقیت ثبت شد Prefix" + "\n" + "لطفا فایلی را که میخواهید Prefix روی آن قرار بگیرد را ارسال کنید:":
        pass

    elif text == pre:
        pass

    elif text == "⚠️ فقط ارسال فایل ([document, video, photo, voice]) مجاز است":
        pass

    elif text == "⚠️ فرمت فایل نامعتبر است":
        pass

    else:
        updatee = update.message
        t = updatee["text"]
        vi = updatee["video"]
        vo = updatee["voice"]
        p = updatee["photo"]
        d = updatee["document"]

        if t != None:
            context.bot.send_message(chat_id=chat_id, text="⚠️ فقط ارسال فایل ([document, video, photo, voice]) مجاز است")

        elif vi != None:
            file_id = update.message.video.file_id
            caption = update.message.caption
            if caption == None:
                caption = ""
            c.execute('insert into Prefix(Prefix, Type, File_id, Caption) values(?,?,?,?)', (pre.lower(), "video", str(file_id), caption))
            con.commit()

            context.bot.send_message(chat_id=chat_id, text="✅ لینک دهی به فایل با موفقیت انجام شد" + "\n" + "لینک:" + "\n" + f"https://t.me/{BOT_ID2}?start={pre.lower()}", disable_web_page_preview=True)
            menu_admin(update, context)
            return STATAD
            

        elif vo != None:
            file_id = update.message.voice.file_id
            caption = update.message.caption
            if caption == None:
                caption = ""
            c.execute('insert into Prefix(Prefix, Type, File_id, Caption) values(?,?,?,?)', (pre.lower(), "voice", str(file_id), caption))
            con.commit()

            context.bot.send_message(chat_id=chat_id, text="✅ لینک دهی به فایل با موفقیت انجام شد" + "\n" + "لینک:" + "\n" + f"https://t.me/{BOT_ID2}?start={pre.lower()}", disable_web_page_preview=True)
            menu_admin(update, context)
            return STATAD

        elif p != None and p != []:
            file_id = update.message.photo[0].file_id
            caption = update.message.caption
            if caption == None:
                caption = ""
            c.execute('insert into Prefix(Prefix, Type, File_id, Caption) values(?,?,?,?)', (pre.lower(), "photo", str(file_id), caption))
            con.commit()

            context.bot.send_message(chat_id=chat_id, text="✅ لینک دهی به فایل با موفقیت انجام شد" + "\n" + "لینک:" + "\n" + f"https://t.me/{BOT_ID2}?start={pre.lower()}", disable_web_page_preview=True)
            menu_admin(update, context)
            return STATAD

        elif d != None:
            file_id = update.message.document.file_id
            caption = update.message.caption
            if caption == None:
                caption = ""
            c.execute('insert into Prefix(Prefix, Type, File_id, Caption) values(?,?,?,?)', (pre.lower(), "document", str(file_id), caption))
            con.commit()

            context.bot.send_message(chat_id=chat_id, text="✅ لینک دهی به فایل با موفقیت انجام شد" + "\n" + "لینک:" + "\n" + f"https://t.me/{BOT_ID2}?start={pre.lower()}", disable_web_page_preview=True)
            menu_admin(update, context)
            return STATAD
        
        else:
            context.bot.send_message(chat_id=chat_id, text="⚠️ فرمت فایل نامعتبر است")
            menu_admin(update, context)
            return STATAD

def getsar(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    if update.message.from_user.is_bot:
        pass

    else:
        if text == ret:
            menu_admin(update, context)
            return STATAD
    
        elif text == "لطفا پیام ([document, video, photo, voice, text]) را برای ارسال سراسری به کاربران بات ارسال کنید:" + "\n" + "\nجان موحدی حواستون باشه پیامی که اینجا میفرستید برای همه اعضا میره هیچ جوره هم نمیشه جلوشو گرفت 🙃":
            pass

        elif text == "📩 ارسال پیام سراسری":
            pass

        elif text == "⚠️ فرمت فایل نامعتبر است":
            pass

        elif text == "❗️ آغاز عملیات ارسال پیام سراسری" + "\n" + "\nبه دلیل محدودیت های تلگرام هر ۲ ثانیه یک پیام ارسال میشود":
            pass

        elif text == "✅ عملیات به پایان رسید":
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
                context.bot.send_message(chat_id=chat_id, text="❗️ آغاز عملیات ارسال پیام سراسری" + "\n" + "\nبه دلیل محدودیت های تلگرام هر ۲ ثانیه یک پیام ارسال میشود", reply_markup=ReplyKeyboardRemove())
                Manage().send_message(from_id=chat_id, mid=mid)
                context.bot.send_message(chat_id=chat_id, text="✅ عملیات به پایان رسید")
                menu_admin(update, context)
                return STATAD

            elif vi != None:
                file_id = update.message.video.file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""
                context.bot.send_message(chat_id=chat_id, text="❗️ آغاز عملیات ارسال پیام سراسری" + "\n" + "\nبه دلیل محدودیت های تلگرام هر ۲ ثانیه یک پیام ارسال میشود", reply_markup=ReplyKeyboardRemove())
                Manage().send_video(video=file_id, caption=caption)
                context.bot.send_message(chat_id=chat_id, text="✅ عملیات به پایان رسید")
                menu_admin(update, context)
                return STATAD
                

            elif vo != None:
                file_id = update.message.voice.file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""
                context.bot.send_message(chat_id=chat_id, text="❗️ آغاز عملیات ارسال پیام سراسری" + "\n" + "\nبه دلیل محدودیت های تلگرام هر ۲ ثانیه یک پیام ارسال میشود", reply_markup=ReplyKeyboardRemove())
                Manage().send_voice(voice=file_id, caption=caption)
                context.bot.send_message(chat_id=chat_id, text="✅ عملیات به پایان رسید")
                menu_admin(update, context)
                return STATAD

            elif p != None and p != []:
                file_id = update.message.photo[0].file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""
                context.bot.send_message(chat_id=chat_id, text="❗️ آغاز عملیات ارسال پیام سراسری" + "\n" + "\nبه دلیل محدودیت های تلگرام هر ۲ ثانیه یک پیام ارسال میشود", reply_markup=ReplyKeyboardRemove())
                Manage().send_photo(photo=file_id, caption=caption)
                context.bot.send_message(chat_id=chat_id, text="✅ عملیات به پایان رسید")
                menu_admin(update, context)
                return STATAD

            elif d != None:
                file_id = update.message.document.file_id
                caption = update.message.caption
                if caption == None:
                    caption = ""
                context.bot.send_message(chat_id=chat_id, text="❗️ آغاز عملیات ارسال پیام سراسری" + "\n" + "\nبه دلیل محدودیت های تلگرام هر ۲ ثانیه یک پیام ارسال میشود", reply_markup=ReplyKeyboardRemove())
                Manage().send_document(document=file_id, caption=caption)
                context.bot.send_message(chat_id=chat_id, text="✅ عملیات به پایان رسید")
                menu_admin(update, context)
                return STATAD
            
            else:
                context.bot.send_message(chat_id=chat_id, text="⚠️ فرمت فایل نامعتبر است")
                menu_admin(update, context)
                return STATAD

def gettakid(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    
    if update.message.from_user.is_bot:
        pass
    
    else:
        if text == ret:
            menu_admin(update, context)
            return STATAD

        elif text == "📩 ارسال پیام تکی":
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
                if Manage().send_message_tak(from_id=chat_id, mid=mid, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
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

                if Manage().send_video_tak(video=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
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

                if Manage().send_voice_tak(voice=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
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

                if Manage().send_photo_tak(photo=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
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

                if Manage().send_document_tak(document=file_id, caption=caption, chat_id=chatsend):
                    context.bot.send_message(chat_id=chat_id, text="✅ با موفقیت ارسال شد")
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

def getban(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    Blocked = Manage().get_block()

    if text == ret:
        menu_admin(update, context)
        return STATAD

    elif text == "🚫 لیست افراد بن شده:" + "\n" + str(Blocked) + "\n" + "برای بن یا آنبن شماره کاربری کاربر نظر را ارسال کنید:":
        pass

    elif text == "🚫 بن و آنبن کاربران":
        pass

    elif text == "⚠️ فرمت نامعتبر":
        pass

    elif text == "✅ کاربر با موفقیت بن شد":
        pass

    elif text == "✅ کاربر با موفقیت آنبن شد":
        pass

    else:
        text = Persian().convert(text=str(text))
        reg = re.compile('^[0-9]+$')
        cr = reg.match(str(text))

        if cr :
            num_id = literal_eval(text)
            c.execute('SELECT * FROM Blocked WHERE Chat_id=?', (num_id,))
            rows = c.fetchall()

            if rows == []:
                c.execute('insert into Blocked(Chat_id) values(?)', (num_id,))
                con.commit()

                context.bot.send_message(chat_id=chat_id, text="✅ کاربر با موفقیت بن شد")
                menu_admin(update, context)

                return STATAD

            else:
                c.execute("DELETE from Blocked where Chat_id=?", (num_id,))
                con.commit()

                context.bot.send_message(chat_id=chat_id, text="✅ کاربر با موفقیت آنبن شد")
                menu_admin(update, context)

                return STATAD

        else:
            context.bot.send_message(chat_id=chat_id, text="⚠️ فرمت نامعتبر")

def gettermbank(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    Blocked = Manage().get_block()

    count = context.user_data.get("usageCount", 0)
    restrict_since = context.user_data.get("restrictSince", 0)
    last_message = context.user_data.get("lastMessage", 0)

    if chat_id not in Blocked and not restrict_since:
        if text == "ترم 1️⃣":
            keyboard = copy(keyboard_doros_term1)
            keyboard.pop(8)
            keyboard.append([KeyboardButton(text=ret), KeyboardButton(text=ret_menu)])

            rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
            sendbankt1(update, context)
            return SENDBANKT1

        elif text == "ترم 2️⃣":
            #Should define new keyboard based on files
            keyboard = copy(keyboard_doros_term2)
            keyboard.pop(13)
            keyboard.append([KeyboardButton(text=ret), KeyboardButton(text=ret_menu)])
            keyboard.pop(7)
            keyboard.pop(10)
            keyboard.pop(10)

            rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
            sendbankt2(update, context)
            return SENDBANKT2

        elif text == ret:
            menu(update, context)
            return STAT

        else:
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")

            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()
    
    elif restrict_since:
        if (time.time() - restrict_since) >= 300: # 5 minutes
            del context.user_data["restrictSince"]
            del context.user_data["usageCount"]
            update.effective_message.reply_text("⚠️ محدودیت شما به اتمام رسید")
        else:
            update.effective_message.reply_text("⚠️ زمان محدودیت شما به اتمام نرسیده است" + "\n" + f"زمان باقی مانده به ثانیه: {str(round(300 - (time.time() - restrict_since)))}")

    else:
        pass

def sendbankt1(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    Blocked = Manage().get_block()

    count = context.user_data.get("usageCount", 0)
    restrict_since = context.user_data.get("restrictSince", 0)
    last_message = context.user_data.get("lastMessage", 0)

    jqt1 = getinfofromjson()["QuestionBankT1"]

    if chat_id not in Blocked and not restrict_since:
        if text == ret_menu:
            menu(update , context)
            return STAT

        elif text == ret:
            rp = ReplyKeyboardMarkup(keyboard_select_term, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا ترم مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)

            return GETTERMBANK
        
        elif text == "علوم تشریح 💀":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["OTN"], caption="📁 نمونه سوالات میان ترم و پایان ترم علوم تشریح نظری" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jqt1["OTA"], caption="📁 نمونه سوالات پایان ترم علوم تشریح عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "بیوشیمی 🧪":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["BioChemystreyN"], caption="📁 نمونه سوالات میان ترم و پایان ترم بیوشیمی نظری" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jqt1["BioChemystreyA"], caption="📁 نمونه سوالات پایان ترم بیوشیمی عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "فیزیولوژی 🔎":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["Physiology"], caption="📁 نمونه سوالات میان ترم و پایان ترم فیزیولوژی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "روانشناسی 🧠":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["Psycology"], caption="📁 نمونه سوالات میان ترم و پایان ترم روانشناسی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "فیزیک پزشکی 😭":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["Medical Physics"], caption="📁 نمونه سوالات میان ترم و پایان ترم فیزیک پزشکی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "فارسی 🇮🇷":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["Persian"], caption="📁 نمونه سوالات میان ترم و پایان ترم ادبیات" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "زبان عمومی " + "1️⃣":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["Eng1"], caption="📁 نمونه سوالات میان ترم و پایان ترم زبان عمومی ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "دانش خانواده 👨‍👩‍👧‍👦":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt1["Danesh"], caption="📁 نمونه سوالات میان ترم و پایان ترم دانش خانواده" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        
        else:
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")

            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()
    
    elif restrict_since:
        if (time.time() - restrict_since) >= 300: # 5 minutes
            del context.user_data["restrictSince"]
            del context.user_data["usageCount"]
            update.effective_message.reply_text("⚠️ محدودیت شما به اتمام رسید")
        else:
            update.effective_message.reply_text("⚠️ زمان محدودیت شما به اتمام نرسیده است" + "\n" + f"زمان باقی مانده به ثانیه: {str(round(300 - (time.time() - restrict_since)))}")

    else:
        pass

def sendbankt2(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    Blocked = Manage().get_block()

    count = context.user_data.get("usageCount", 0)
    restrict_since = context.user_data.get("restrictSince", 0)
    last_message = context.user_data.get("lastMessage", 0)

    jqt2 = getinfofromjson()["QuestionBankT2"]

    if chat_id not in Blocked and not restrict_since:
        if text == ret_menu:
            menu(update , context)
            return STAT

        elif text == ret:
            rp = ReplyKeyboardMarkup(keyboard_select_term, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا ترم مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)

            return GETTERMBANK

        elif text == "دستگاه قلب 🫀":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Ghalb"], caption="📁 نمونه سوالات میان ترم و پایان ترم دستگاه قلب" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                
        elif text == "دستگاه تنفس 🫁":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Tanafos"], caption="📁 نمونه سوالات میان ترم و پایان ترم دستگاه تنفس" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "دستگاه غدد 🌋":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Ghodad"], caption="📁 نمونه سوالات میان ترم و پایان ترم دستگاه غدد" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jqt2["GhodadQoloompaye"], caption="📄 نمونه سوالات علوم پایه دستگاه غدد" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "بیوشیمی دیسیپلین 🧪":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["BioChemystreyDN"], caption="📁 نمونه سوالات میان ترم و پایان ترم بیوشیمی دیسیپلین نظری" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
                context.bot.send_document(chat_id=chat_id, document=jqt2["BioChemystreyDA"], caption="📁 نمونه سوالات پایان ترم بیوشیمی دیسیپلین عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "علوم تشریح عملی 💀":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["OTA2"], caption="📁 نمونه سوالات پایان ترم علوم تشریح عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "فیزیولوژی عملی 🔎":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["PhysiologyA"], caption="📁 نمونه سوالات پایان ترم فیزیولوژی عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "تغذیه 🍫":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Taghziye"], caption="📁 نمونه سوالات میان ترم و پایان ترم اصول تغذیه " + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "زبان عمومی " + "2️⃣":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Eng2"], caption="📁 نمونه سوالات میان ترم و پایان ترم زبان عمومی ۲ " + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "اندیشه اسلامی 📿":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Andisheh"], caption="📁 نمونه سوالات میان ترم و پایان ترم اندیشه اسلامی ۱ " + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

        elif text == "انقلاب اسلامی 🕋":
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")
            
            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

                context.bot.send_document(chat_id=chat_id, document=jqt2["Enghelab"], caption="📁 نمونه سوالات میان ترم و پایان ترم انقلاب اسلامی " + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        
        else:
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")

            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()

    elif restrict_since:
        if (time.time() - restrict_since) >= 300: # 5 minutes
            del context.user_data["restrictSince"]
            del context.user_data["usageCount"]
            update.effective_message.reply_text("⚠️ محدودیت شما به اتمام رسید")
        else:
            update.effective_message.reply_text("⚠️ زمان محدودیت شما به اتمام نرسیده است" + "\n" + f"زمان باقی مانده به ثانیه: {str(round(300 - (time.time() - restrict_since)))}")

    else:
        pass

def dt1(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    Blocked = Manage().get_block()

    keyboard_wv = [
    [KeyboardButton(text="جزوه / منابع 📔")],
    [KeyboardButton(text="امتحان ۱۴۰۰ 📕")],
    [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
    ]

    count = context.user_data.get("usageCount", 0)
    restrict_since = context.user_data.get("restrictSince", 0)
    last_message = context.user_data.get("lastMessage", 0)

    if chat_id not in Blocked and not restrict_since:
        if text == "علوم تشریح 💀":
            keyboard = [
                [KeyboardButton(text="علوم تشریح نظری 💀")],
                [KeyboardButton(text="علوم تشریح عملی 💀")],
                [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
            ]

            rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup=rp)
            chooseot(update, context)
            return CHOT

        elif text == "بیوشیمی 🧪":
            keyboard = [
                [KeyboardButton(text="بیوشیمی نظری 🧪")],
                [KeyboardButton(text="بیوشیمی عملی 🧪")],
                [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
            ]

            rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup=rp)
            choosebio(update, context)
            return CHBIO

        elif text == "فیزیولوژی 🔎":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
            choosesendphysio(update, context)
            return CHSP

        elif text == "روانشناسی 🧠":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
            choosesendravan(update, context)
            return CHSR

        elif text == "فیزیک پزشکی 😭":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
            choosesendphysic(update, context)
            return CHSPH

        elif text == "فارسی 🇮🇷":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_wv, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
            choosesendpersian(update, context)
            return CHSPE

        elif text == "زبان عمومی " + "1️⃣":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_wv, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
            choosesendenglish1(update, context)
            return CHSE1

        elif text == "دانش خانواده 👨‍👩‍👧‍👦":
            rp = ReplyKeyboardMarkup(keyboard=keyboard_wv, resize_keyboard=True)
            context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
            choosesenddanesh(update, context)
            return CHSDA
        
        elif text == ret:
            menu(update, context)
            return STAT
        
        else:
            if count == MAX_USAGE:
                if chat_id not in Admins:
                    context.user_data["restrictSince"] = time.time()
                    update.effective_message.reply_text("⚠️ به علت اسپم شما به مدت ۵ دقیقه از بات بلاک شدید")

            else:
                if chat_id not in Admins:
                    if (time.time() - last_message) < 5:
                        context.user_data["usageCount"] = count + 1
                        context.user_data["lastMessage"] = time.time()

                    else:
                        context.user_data["lastMessage"] = time.time()
    
    elif restrict_since:
        if (time.time() - restrict_since) >= 300: # 5 minutes
            del context.user_data["restrictSince"]
            del context.user_data["usageCount"]
            update.effective_message.reply_text("⚠️ محدودیت شما به اتمام رسید")
        else:
            update.effective_message.reply_text("⚠️ زمان محدودیت شما به اتمام نرسیده است" + "\n" + f"زمان باقی مانده به ثانیه: {str(round(300 - (time.time() - restrict_since)))}")

    else:
        pass

def choosebio(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == "بیوشیمی نظری 🧪":

        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        choosesendbion(update, context)
        return CHSBION

    elif text == "بیوشیمی عملی 🧪":
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        choosesendbioa(update, context)
        return CHSBIOA

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def chooseot(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == "علوم تشریح نظری 💀":
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)

        choosesendotn(update, context)
        return CHSOTN

    elif text == "علوم تشریح عملی 💀":
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
    
        choosesendota(update, context)
        return CHSOTA

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendota(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js1 = getinfofromjson()["OTA"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 Epithelium")],
            [KeyboardButton(text="🎞 Connective")],
            [KeyboardButton(text="🎞 Muscle & Blood")],
            [KeyboardButton(text="🎞 Bone & Cartilage")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideoota(update, context)
        return CHSVOTA

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js1["jozve"], caption="📁 تمامی جزوه ها و منابع مربوط به درس علوم تشریح عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        context.bot.send_document(chat_id=chat_id, document=js1["exam"], caption="📄 امتحان پایان ترم علوم تشریح عملی مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendotn(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js1 = getinfofromjson()["OTN"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 Introduction to Anatomy")],
            [KeyboardButton(text="🎞 Joints")],
            [KeyboardButton(text="🎞 Sternum & Ribs")],
            [KeyboardButton(text="🎞 Vertebral Column")],
            [KeyboardButton(text="🎞 Skull & Nasal")],
            [KeyboardButton(text="🎞 Muscular & Vascular")],
            [KeyboardButton(text="🎞 جلسه پرسش و پاسخ")],
            [KeyboardButton(text="🎞 Cell 1")],
            [KeyboardButton(text="🎞 Cell 2")],
            [KeyboardButton(text="🎞 Cell 3")],
            [KeyboardButton(text="🎞 Muscle")],
            [KeyboardButton(text="🎞 Blood")],
            [KeyboardButton(text="🎞 First Week")],
            [KeyboardButton(text="🎞 Placenta")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideootn(update, context)
        return CHSVOTN

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js1["jozve"], caption="📁 تمامی جزوه ها و منابع مربوط به درس علوم تشریح نظری" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        exam_l = js1["exam"]
        context.bot.send_document(chat_id=chat_id, document=exam_l[0], caption="📄 امتحان میان ترم علوم تشریح نظری مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=exam_l[1], caption="📄 امتحان پایان ترم علوم تشریح نظری مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendbioa(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js1 = getinfofromjson()["BioChemystreyA"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 Lab Introduction")],
            [KeyboardButton(text="🎞 Carbohydrate")],
            [KeyboardButton(text="🎞 Amino Acid & Protein")],
            [KeyboardButton(text="🎞 Casein IEP")],
            [KeyboardButton(text="🎞 PCR")],
            [KeyboardButton(text="🎞 Electrophoresis")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideobioa(update, context)
        return CHSVBIOA

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js1["jozve"], caption="📄 جزوه بیوشیمی عملی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        context.bot.send_document(chat_id=chat_id, document=js1["exam"], caption="📄 امتحان پایان ترم بیوشیمی عملی مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendbion(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js1 = getinfofromjson()["BioChemystreyN"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 Carbohydrate 1")],
            [KeyboardButton(text="🎞 Carbohydrate 2")],
            [KeyboardButton(text="🎞 Water & Buffer")],
            [KeyboardButton(text="🎞 Nucleic Acid")],
            [KeyboardButton(text="🎞 Lipid 1")],
            [KeyboardButton(text="🎞 Lipid 2")],
            [KeyboardButton(text="🎞 Enzyme 1")],
            [KeyboardButton(text="🎞 Enzyme 2")],
            [KeyboardButton(text="🎞 Vitamin")],
            [KeyboardButton(text="🎞 Proteins of Plasma")],
            [KeyboardButton(text="🎞 Replication")],
            [KeyboardButton(text="🎞 Translation")],
            [KeyboardButton(text="🎞 Transcription")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideobion(update, context)
        return CHSVBION

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js1["jozve"], caption="📁 تمامی جزوه ها و منابع مربوط به درس بیوشیمی نظری" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        exam_l = js1["exam"]
        context.bot.send_document(chat_id=chat_id, document=exam_l[0], caption="📄 امتحان میان ترم بیوشیمی نظری مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=exam_l[1], caption="📄 امتحان پایان ترم بیوشیمی نظری مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendphysio(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js1 = getinfofromjson()["Physiology"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 Introduciotion to Cell")],
            [KeyboardButton(text="🎞 Osmosis")],
            [KeyboardButton(text="🎞 Ione Equilibrum")],
            [KeyboardButton(text="🎞 Action Potential 1")],
            [KeyboardButton(text="🎞 Action Potential 2")],
            [KeyboardButton(text="🎞 Synapse")],
            [KeyboardButton(text="🎞 Muscle 1")],
            [KeyboardButton(text="🎞 Muscle 2")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideophysio(update, context)
        return CHSVP

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js1["jozve"], caption="📁 تمامی جزوه ها و منابع مربوط به درس فیزیولوژی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        context.bot.send_document(chat_id=chat_id, document=js1["exam"], caption="📄 امتحان پایان ترم فیزیولوژی مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass
  
def choosesendravan(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js2 = getinfofromjson()["Psycology"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 جلسه اول")],
            [KeyboardButton(text="🎞 جلسه دوم")],
            [KeyboardButton(text="🎞 جلسه سوم")],
            [KeyboardButton(text="🎞 جلسه پرسش و پاسخ")],
            [KeyboardButton(text="🎞 جلسه پنجم")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideoravan(update, context)
        return CHSVR

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js2["jozve"], caption="📁 تمامی جزوه ها و منابع مربوط به درس روانشناسی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        context.bot.send_document(chat_id=chat_id, document=js2["exam"], caption="📄 امتحان پایان ترم روانشناسی مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendphysic(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js3 = getinfofromjson()["Medical Physics"]

    if text == "کلاس ضبطی / فایل های ویدئویی 🎥":
        keyboard = [
            [KeyboardButton(text="🎞 رادیولوژی ۱")],
            [KeyboardButton(text="🎞 رادیولوژی ۲")],
            [KeyboardButton(text="🎞 سی تی اسکن")],
            [KeyboardButton(text="🎞 حفاظت در برابر پرتو های یونساز")],
            [KeyboardButton(text="🎞 پزشکی هسته ای ۱")],
            [KeyboardButton(text="🎞 پزشکی هسته ای ۲")],
            [KeyboardButton(text="🎞 پزشکی هسته ای ۳")],
            [KeyboardButton(text="🎞 رادیوبیولوژی")],
            [KeyboardButton(text="🎞 نور و چشم پزشکی ۱")],
            [KeyboardButton(text="🎞 نور و چشم پزشکی ۲")],
            [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
        ]
        rp = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا مبحث مورد نظر را انتخاب کنید:", reply_markup=rp)

        choosesendvideophysic(update, context)
        return CHSVPH

    elif text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js3["jozve"], caption="📁 تمامی جزوه ها و منابع مربوط به درس فیزیک پزشکی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        exam_l = js3["exam"]
        context.bot.send_document(chat_id=chat_id, document=exam_l[0], caption="📄 امتحان میان ترم فیزیک پزشکی مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=exam_l[1], caption="📄 امتحان پایان ترم فیزیک پزشکی مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendpersian(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js4 = getinfofromjson()["Persian"]

    if text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js4["jozve"], caption="📄 جزوه ادبیات" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        exam_l = js4["exam"]
        context.bot.send_document(chat_id=chat_id, document=exam_l[0], caption="📄 امتحان میان ترم ادبیات مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=exam_l[1], caption="📄 امتحان پایان ترم ادبیات مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendenglish1(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js5 = getinfofromjson()["Eng1"]

    if text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js5["jozve"], caption="📚 کتاب Improving Reading Skill" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        exam_l = js5["exam"]
        context.bot.send_document(chat_id=chat_id, document=exam_l[0], caption="📄 امتحان میان ترم زبان عمومی ۱ مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=exam_l[1], caption="📄 امتحان پایان ترم زبان عمومی ۱ مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesenddanesh(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    js6 = getinfofromjson()["Danesh"]

    if text == "جزوه / منابع 📔":
        context.bot.send_document(chat_id=chat_id, document=js6["jozve"], caption="📚 کتاب دانش خانواده و جمعیت" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "امتحان ۱۴۰۰ 📕":
        exam_l = js6["exam"]
        context.bot.send_document(chat_id=chat_id, document=exam_l[0], caption="📄 امتحان میان ترم دانش خانواده مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=exam_l[1], caption="📄 امتحان پایان ترم دانش خانواده مهر ۱۴۰۰" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_doros_term1, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا درس مورد نظر را از منوی زیر انتخاب کنید:", reply_markup=rp)
        return DOROST1
    
    else:
        pass

def choosesendvideobion(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["BioChemystreyN"]["videos"]

    if text == "🎞 Carbohydrate 1":
        context.bot.send_video(chat_id=chat_id, video=jv["Carbo1"], caption="🎬 کربوهیدرات ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Carbohydrate 2":
        context.bot.send_document(chat_id=chat_id, document=jv["Carbo2 P1 Doc"], caption="🎬 کربوهیدرات ۲ پارت ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_document(chat_id=chat_id, document=jv["Carbo2 P2 Doc"], caption="🎬 کربوهیدرات ۲ پارت ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Water & Buffer":
        context.bot.send_video(chat_id=chat_id, video=jv["Buffer"], caption="🎬 آب و بافر" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Nucleic Acid":
        context.bot.send_video(chat_id=chat_id, video=jv["Nucleic Acid"], caption="🎬 نوکلئیک اسید" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Lipid 1":
        context.bot.send_video(chat_id=chat_id, video=jv["Lipid1"], caption="🎬 لیپید ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Lipid 2":
        context.bot.send_video(chat_id=chat_id, video=jv["Lipid2"], caption="🎬 لیپید ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Enzyme 1":
        context.bot.send_video(chat_id=chat_id, video=jv["Enzyme1"], caption="🎬 آنزیم ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Enzyme 2":
        context.bot.send_video(chat_id=chat_id, video=jv["Enzyme2"], caption="🎬 آنزیم ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Vitamin":
        context.bot.send_video(chat_id=chat_id, video=jv["Vitamin"], caption="🎬 ویتامین" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
    
    elif text == "🎞 Proteins of Plasma":
        context.bot.send_video(chat_id=chat_id, video=jv["Plasma"], caption="🎬 پروتیئن های پلاسما" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
    
    elif text == "🎞 Replication":
        context.bot.send_video(chat_id=chat_id, video=jv["Replication"], caption="🎬 همانند سازی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Translation":
        context.bot.send_video(chat_id=chat_id, video=jv["Translation"], caption="🎬 ترجمه" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Transcription":
        context.bot.send_video(chat_id=chat_id, video=jv["Transcription"], caption="🎬 رونویسی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSBION

    else:
        pass

def choosesendvideobioa(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["BioChemystreyA"]["videos"]

    if text == "🎞 Lab Introduction":
        vidl = jv["Labintro"]
        for i in vidl:
            context.bot.send_video(chat_id=chat_id, video=i, caption="🎬 Lab Introduction" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Carbohydrate":
        vidl = jv["Carbo"]
        for i in vidl:
            context.bot.send_video(chat_id=chat_id, video=i, caption="🎬 Carbohydrate" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Amino Acid & Protein":
        vidl = jv["Amino & Protein"]
        for i in vidl:
            context.bot.send_video(chat_id=chat_id, video=i, caption="🎬 Amino Acid & Protein" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Casein IEP":
        vidl = jv["Casein iep Doc"]
        for i in vidl:
            context.bot.send_document(chat_id=chat_id, document=i, caption="🎬 Casein IEP" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 PCR":
        context.bot.send_video(chat_id=chat_id, video=jv["PCR"], caption="🎬 PCR" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Electrophoresis":
        vidl = jv["Electrophoresis"]
        for i in vidl:
            context.bot.send_video(chat_id=chat_id, video=i, caption="🎬 Electrophoresis" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSBIOA

    else:
        pass

def choosesendvideootn(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["OTN"]["videos"]

    if text == "🎞 Introduction to Anatomy":
        context.bot.send_video(chat_id=chat_id, video=jv["Intro"], caption="🎬 آشنایی با آناتومی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        
    elif text == "🎞 Joints":
        context.bot.send_video(chat_id=chat_id, video=jv["Joint"][0], caption="🎬 آشنایی با مفاصل" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Joint"][1], caption="🎬 مفاصل تنه" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Sternum & Ribs":
        context.bot.send_video(chat_id=chat_id, video=jv["Sternum & Ribs"], caption="🎬 دنده ها و استخوان جناغ" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Vertebral Column":
        context.bot.send_video(chat_id=chat_id, video=jv["Vertebral"][0], caption="🎬 ستون مهره ها ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Vertebral"][1], caption="🎬 ستون مهره ها ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Skull & Nasal":
        context.bot.send_video(chat_id=chat_id, video=jv["Skull & Nasal"][0], caption="🎬 جمجمه" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Skull & Nasal"][1], caption="🎬 حفره بینی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Muscular & Vascular":
        context.bot.send_video(chat_id=chat_id, video=jv["Muscular & Vascular"][0], caption="🎬 ماهیچه" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Muscular & Vascular"][1], caption="🎬 عروق" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 جلسه پرسش و پاسخ":
        context.bot.send_video(chat_id=chat_id, video=jv["Q&A"], caption="🎬 جلسه پرسش و پاسخ" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Cell 1":
        context.bot.send_video(chat_id=chat_id, video=jv["Cell1"], caption="🎬 سلول ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Cell 2":
        context.bot.send_video(chat_id=chat_id, video=jv["Cell2"], caption="🎬 سلول ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Cell 3":
        context.bot.send_video(chat_id=chat_id, video=jv["Cell3"], caption="🎬 سلول ۳" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Muscle":
        context.bot.send_video(chat_id=chat_id, video=jv["Muscle"], caption="🎬 ماهیچه" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Blood":
        context.bot.send_video(chat_id=chat_id, video=jv["Blood"], caption="🎬 خون" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 First Week":
        context.bot.send_video(chat_id=chat_id, video=jv["FirstWeek"], caption="🎬 هفته اول جنین" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Placenta":
        context.bot.send_video(chat_id=chat_id, video=jv["Placenta"], caption="🎬 پلاسنتا" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSOTN

    else:
        pass

def choosesendvideoota(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["OTA"]["videos"]

    keyboard = [
        [KeyboardButton(text="🎞 Epithelium")],
        [KeyboardButton(text="🎞 Connective")],
        [KeyboardButton(text="🎞 Muscle & Blood")],
        [KeyboardButton(text="🎞 Bone & Cartilage")],
        [KeyboardButton(text=ret), KeyboardButton(text=ret_menu)]
    ]

    if text == "🎞 Epithelium":
        context.bot.send_video(chat_id=chat_id, video=jv["Epithelium"], caption="🎬 بافت پوششی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Connective":
        context.bot.send_video(chat_id=chat_id, video=jv["Connective"], caption="🎬 بافت پیوندی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Muscle & Blood":
        context.bot.send_video(chat_id=chat_id, video=jv["Muscular & Blood"], caption="🎬 ماهیچه و خون" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Bone & Cartilage":
        context.bot.send_video(chat_id=chat_id, video=jv["Bone & Cartilage"], caption="🎬 استخوان و غضروف" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSOTA

    else:
        pass

def choosesendvideophysio(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["Physiology"]["videos"]

    if text == "🎞 Introduciotion to Cell":
        context.bot.send_video(chat_id=chat_id, video=jv["Introduciotion to Cell P1"], caption="🎬 Introduciotion to Cell P1" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Introduciotion to Cell P2"], caption="🎬 Introduciotion to Cell P2" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Osmosis":
        context.bot.send_video(chat_id=chat_id, video=jv["Osmosis"], caption="🎬 اسمز" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Ione Equilibrum":
        context.bot.send_video(chat_id=chat_id, video=jv["Ione Equilibrum"], caption="🎬 تعادل یونی" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Action Potential 1":
        context.bot.send_video(chat_id=chat_id, video=jv["Action Potential1"], caption="🎬 پتانسیل عمل ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Action Potential 2":
        context.bot.send_video(chat_id=chat_id, video=jv["Action Potential2"], caption="🎬 پتانسیل عمل ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Synapse":
        context.bot.send_video(chat_id=chat_id, video=jv["Synapse"], caption="🎬 سیناپس" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Muscle 1":
        context.bot.send_video(chat_id=chat_id, video=jv["Muscle1"], caption="🎬 ماهیچه ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 Muscle 2":
        context.bot.send_video(chat_id=chat_id, video=jv["Muscle2"], caption="🎬 ماهیچه ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSP

    else:
        pass

def choosesendvideoravan(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["Psycology"]["videos"]

    if text == "🎞 جلسه اول":
        context.bot.send_video(chat_id=chat_id, video=jv["J1"], caption="🎬 جلسه اول" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 جلسه دوم":
        context.bot.send_video(chat_id=chat_id, video=jv["J2"], caption="🎬 جلسه دوم" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 جلسه سوم":
        context.bot.send_video(chat_id=chat_id, video=jv["J3 P1"], caption="🎬 جلسه سوم پارت ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["J3 P2"], caption="🎬 جلسه سوم پارت ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 جلسه پرسش و پاسخ":
        context.bot.send_video(chat_id=chat_id, video=jv["Q&A"], caption="🎬 جلسه پرسش و پاسخ" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 جلسه پنجم":
        context.bot.send_video(chat_id=chat_id, video=jv["J5"], caption="🎬 جلسه پنجم" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSR

    else:
        pass

def choosesendvideophysic(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    jv = getinfofromjson()["Medical Physics"]["videos"]

    if text == "🎞 رادیولوژی ۱":
        context.bot.send_document(chat_id=chat_id, document=jv["Movahedi1 Doc"], caption="🎬 رادیولوژی ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 رادیولوژی ۲":
        context.bot.send_video(chat_id=chat_id, video=jv["Movahedi2"], caption="🎬 رادیولوژی ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 سی تی اسکن":
        context.bot.send_video(chat_id=chat_id, video=jv["Movahedi3"], caption="🎬 سی تی اسکن" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 حفاظت در برابر پرتو های یونساز":
        context.bot.send_video(chat_id=chat_id, video=jv["Movahedi4"], caption="🎬 حفاظت در برابر پرتو های یونساز" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 پزشکی هسته ای ۱":
        context.bot.send_video(chat_id=chat_id, video=jv["Mortazavi1 P1"], caption="🎬 پزشکی هسته ای ۱ پارت ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Mortazavi1 P2"], caption="🎬 پزشکی هسته ای ۱ پارت ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 پزشکی هسته ای ۲":
        context.bot.send_video(chat_id=chat_id, video=jv["Mortazavi2"], caption="🎬 پزشکی هسته ای ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 پزشکی هسته ای ۳":
        context.bot.send_video(chat_id=chat_id, video=jv["Mortazavi3"], caption="🎬 پزشکی هسته ای ۳" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 رادیوبیولوژی":
        context.bot.send_video(chat_id=chat_id, video=jv["Mehdizadeh1 P1"], caption="🎬 رادیوبیولوژی پارت ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")
        context.bot.send_video(chat_id=chat_id, video=jv["Mehdizadeh1 P2"], caption="🎬 رادیوبیولوژی پارت ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 نور و چشم پزشکی ۱":
        context.bot.send_video(chat_id=chat_id, video=jv["Mehdizadeh2"], caption="🎬 نور و چشم پزشکی ۱" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == "🎞 نور و چشم پزشکی ۲":
        context.bot.send_video(chat_id=chat_id, video=jv["Mehdizadeh3"], caption="🎬 نور و چشم پزشکی ۲" + "\n\n🤖 ربات تلگرام ورودی مهر ۱۴۰۰ پزشکی شیراز:" + f"\n{BOT_ID}")

    elif text == ret_menu:
        menu(update, context)
        return STAT

    elif text == ret:
        rp = ReplyKeyboardMarkup(keyboard=keyboard_send, resize_keyboard=True)
        context.bot.send_message(chat_id=chat_id, text="لطفا یک گزینه را انتخاب نمایید:", reply_markup = rp)
        return CHSPH

    else:
        pass

def checksys(update, context):
    chat_id = update.message.chat_id

    try:
        res = getrequests(f'{SITE_ADDRESS}/v1/check').json()
    
    except:
        res = "Error !"

    if chat_id in Admins:
        context.bot.send_message(chat_id=chat_id, text=str(res))
    
    else:
        pass

def cancel(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="Bikhial Sho Haji")

def error_handle(update, context):
    for i in Admins:
        context.bot.send_message(chat_id=i, text=str(context.error))

def main():
    #Change Before Config
    token = config.MAIN_BOT_TOKEN

    updater = Updater(token=token, workers=16)
    
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STAT : [MessageHandler(Filters.text, stat)],
            DOROST1 : [MessageHandler(Filters.text, dt1)],
            CHBIO : [MessageHandler(Filters.text, choosebio)],
            CHOT : [MessageHandler(Filters.text, chooseot)],
            CHSOTA : [MessageHandler(Filters.text, choosesendota)],
            CHSOTN : [MessageHandler(Filters.text, choosesendotn)],
            CHSBIOA : [MessageHandler(Filters.text, choosesendbioa)],
            CHSBION : [MessageHandler(Filters.text, choosesendbion)],
            CHSP : [MessageHandler(Filters.text, choosesendphysio)],
            CHSR : [MessageHandler(Filters.all, choosesendravan)],
            CHSPH : [MessageHandler(Filters.text, choosesendphysic)],
            CHSPE : [MessageHandler(Filters.text, choosesendpersian)],
            CHSE1 : [MessageHandler(Filters.text, choosesendenglish1)],
            CHSDA : [MessageHandler(Filters.text, choosesenddanesh)],
            CHSVBION:[MessageHandler(Filters.text, choosesendvideobion)],
            CHSVBIOA:[MessageHandler(Filters.text, choosesendvideobioa)],
            CHSVOTN:[MessageHandler(Filters.text, choosesendvideootn)],
            CHSVOTA:[MessageHandler(Filters.text, choosesendvideoota)],
            CHSVP:[MessageHandler(Filters.text, choosesendvideophysio)],
            CHSVR:[MessageHandler(Filters.text, choosesendvideoravan)],
            CHSVPH:[MessageHandler(Filters.text, choosesendvideophysic)],
            STATAD:[MessageHandler(Filters.text, statadmin)],
            GETSAR:[MessageHandler(Filters.all, getsar)],
            GETTAK:[MessageHandler(Filters.all, gettak)],
            GETTAKID:[MessageHandler(Filters.text, gettakid)],
            GETBAN:[MessageHandler(Filters.text, getban)],
            GETPRE:[MessageHandler(Filters.text, getpre)],
            GETPREFILE:[MessageHandler(Filters.all, getprefile)],
            GETPREDEL:[MessageHandler(Filters.text, getpredel)],
            GETTERMBANK:[MessageHandler(Filters.text, gettermbank)],
            SENDBANKT1 : [MessageHandler(Filters.text, sendbankt1)],
            SENDBANKT2 : [MessageHandler(Filters.text, sendbankt2)],
            GETTERMCATEG : [MessageHandler(Filters.text, gettermcateg)]
            
        },
        

        fallbacks=[CommandHandler('harkiinobezanekhare', cancel)],

        allow_reentry=True,

        name="conv_handler",

        run_async=True
        
    )

    dispatcher.add_handler(CommandHandler('checksys', checksys))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error_handle)

    updater.start_polling()
    updater.idle()

if 4 == 4:
    main()