import telebot
from .config import Config


def send_message(text):
    if Config.SEND:
        bot = telebot.TeleBot(Config.TOKEN)
        for chat in Config.chats:
            bot.send_message(chat, text)
    else:
        print(text)
