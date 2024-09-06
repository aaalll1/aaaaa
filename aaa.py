import telebot

# Create a bot object
bot = telebot.TeleBot('7249491605:AAFHyPh2nZHOhEjTDTCKG81yNhoJJwDnBhU')

# Add a handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    # Send a welcome message
    bot.send_message(message.chat.id, 'مرحباً بك! اكتب "السلام عليكم" لأحييك.')

# Add a handler for messages that contain the phrase "السلام عليكم"
@bot.message_handler(func=lambda message: 'السلام عليكم' in message.text)
def greet(message):
    # Respond with "وعليكم السلام تاج راسي علوش"
    bot.send_message(message.chat.id, "وعليكم السلام تاج راسي علوش")

# Start polling Telegram servers
bot.polling()
