import telebot
import threading
from .config import Config


def send_message(text, face=None):
    if Config.SEND:
        bot = telebot.TeleBot(Config.TOKEN)
        for chat in Config.chats:
            bot.send_message(chat, text)
        # send message to listeners
    # else:
    #     print(text)


def run_bot():
    bot = telebot.TeleBot(Config.TOKEN)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        parts = message.text.split()
        if len(parts) == 1 and parts[0] in ['/help', '/start']:
            answer = 'Это бот для системы «свой-чужой».\nЧтобы получать уведомления отправьте /add <выданный id>.'
        elif message.text == '/add':
            answer = 'После команды /add нужно написать выданный id.'
        elif len(parts) == 2 and parts[0] == '/add':
            try:
                face = int(parts[1])
                found = True    # find id in DB
                if not found:
                    raise ValueError
                else:
                    # add listeners
                    answer = 'Теперь Вам будут приходить уведомления про лицо {}.'.format(face)
            except Exception:
                answer = 'Вы написали некорректный id :('
        else:
            answer = 'Я Вас не понимаю, отправьте /help для получения помощи.'
        bot.send_message(message.from_user.id, answer)

    t = threading.Thread(target=bot.polling, daemon=True)
    t.start()
