import subprocess
import sys

def install_packages():
    packages = ['pyTelegramBotAPI', 'instaloader']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    print("المكتبات تم تحميلها بنجاح ✅️")

install_packages()

import telebot
import instaloader
import os
import json
import time

TOKEN = '7249491605:AAFHyPh2nZHOhEjTDTCKG81yNhoJJwDnBhU'
bot = telebot.TeleBot(TOKEN)
#لا تنسى تحط ايديك بالسطر 89

loader = instaloader.Instaloader()
RATINGS_FILE = 'ratings.json'

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_ratings(ratings):
    with open(RATINGS_FILE, 'w') as file:
        json.dump(ratings, file)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "<b>مرحبا بك يا عزيزي ♡... !</b>\n\n"
        "أنا بوت لتحميل مقاطع الفيديو من إنستجرام.\n"
        "لتحميل فيديو، أرسل لي رابط الفيديو من إنستجرام وسأقوم بتحميله لك.\n\n"
        "𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳\n\n"
        "<b>للقيام بذلك:</b>\n"
        "1. أرسل رابط الفيديو الذي ترغب في تحميله.\n"
        "2. انتظر قليلاً حتى يتم تحميل الفيديو.\n"
        "3. سأرسل لك الفيديو بعد تحميله.\n\n"
        "𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳\n"
        "<b>المطور  ~⪼ : ⦅ @iita25 ⦆</b>\n\n"
        "<b>لتقييم البوت، اكتب تقييم</b>"
    )
    bot.reply_to(message, welcome_message, parse_mode='HTML')

@bot.message_handler(func=lambda message: 'تقييم' in message.text)
def rate_bot(message):
    chat_id = message.chat.id
    ratings = load_ratings()
    average_rating = (sum(ratings.values()) / len(ratings)) if ratings else 0
    stars = '⭐' * round(average_rating)
    rating_text = (
        f"<b>☆︙تقييمك للبوت : {stars} ({average_rating:.1f})\n"
        f"☆︙عدد المشاركين في التقييم : ⦅ {len(ratings)} ⦆\n\n"
        "☆︙يرجى تقييم البوت من الأزرار 🩵👇🏻</b>"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(1, 6):
        markup.add(telebot.types.InlineKeyboardButton(f"{'⭐' * i}", callback_data=str(i)))
    markup.add(telebot.types.InlineKeyboardButton("⦅ الصفحة الرئيسية ⦆", callback_data="back"))
    bot.send_message(chat_id, rating_text, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def handle_rating(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    rating = int(call.data)
    ratings = load_ratings()
    ratings[chat_id] = rating
    save_ratings(ratings)
    average_rating = (sum(ratings.values()) / len(ratings)) if ratings else 0
    stars = '⭐' * round(average_rating)
    rating_text = (
        f"<b>شكرا لتقييمك\n\n"
        f"{stars} ({average_rating:.1f})</b>"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("⦅ إعادة التقييم ⦆", callback_data="rate"))
    markup.add(telebot.types.InlineKeyboardButton("⦅ الصفحة الرئيسية ⦆", callback_data="back"))
    bot.edit_message_text(rating_text, chat_id, message_id, parse_mode='HTML', reply_markup=markup)
    bot.send_message(
        "7275336620", #هنا حط ايديك عشان يجيك اشعار على بوتك
        f"*تم تقييم البوت من {call.from_user.first_name}*\n"
        f"تقييمه للبوت {rating} = ⭐\n"
        f"☆︙المعرف [@{call.from_user.username}]\n"
        f"☆︙الايدي {chat_id}", 
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "back")
def go_back(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    send_welcome(telebot.types.Message(chat_id=chat_id, message_id=message_id))

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if 'instagram.com' in url:
        loading_message = bot.reply_to(message, '<b>انتظر، جار تحميل الفيديو...  ♻️ .</b>', parse_mode='HTML')
        dots = ['.', '..', '...']
        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            file_path = 'video.mp4'
            loader.download_post(post, target='video')
            video_files = [f for f in os.listdir('video') if f.endswith('.mp4')]
            if video_files:
                video_path = os.path.join('video', video_files[0])
                with open(video_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)
                os.remove(video_path)
            else:
                bot.reply_to(message, '<b>لم أتمكن من العثور على الفيديو.</b>', parse_mode='HTML')
            os.rmdir('video')
        except Exception as e:
            bot.reply_to(message, (
                '<b>↯︙ لا تنسى الاشتراك بقناتنا حتى يوصلك كل جديد ✅️</b>\n\n'
                '<b>↯︙ @py_giga ..</b>\n\n'
                '<b>↯︙لو ما جاك الفيديو رسل الرابط مرة ثانية ✅️</b>\n\n'
                f'<b>{str(e)}</b>'
            ), parse_mode='HTML')
        finally:
            for _ in range(10):  
                for i in range(3):  
                    bot.edit_message_text(f'<b>انتظر، جار تحميل الفيديو{"." * (i + 1)} ♻️ .</b>', message.chat.id, loading_message.message_id, parse_mode='HTML')
                    time.sleep(0.5)  

print("البوت يعمل بنجاح ✅️")
bot.polling()
