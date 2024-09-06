import telebot

# Create a bot object
bot = telebot.TeleBot('7249491605:AAFHyPh2nZHOhEjTDTCKG81yNhoJJwDnBhU')

# Add a handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    # Send a welcome message
    bot.send_message(message.chat.id, 'مرحبا!')

# Start polling Telegram servers
bot.polling()
