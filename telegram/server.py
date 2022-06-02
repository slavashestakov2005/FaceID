import telebot
import threading
from .config import Config
from server.database.listener import ListenersTable, Listener
from server.database.face import FacesTable


class Bot:
    @staticmethod
    def run_bot():
        Bot.bot = telebot.TeleBot(Config.TOKEN)

        @Bot.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            chat = message.from_user.id
            parts = message.text.split()
            if len(parts) == 1 and parts[0] in ['/help', '/start']:
                answer = '''Это бот для системы «свой-чужой».
Чтобы получать уведомления отправьте /add <выданный id>.
Чтобы отписаться от уведомлений отправьте /delete <выданный id>'''
            elif len(parts) == 1 and parts[0] == '/add':
                answer = 'После команды /add нужно написать выданный id.'
            elif len(parts) == 2 and parts[0] == '/add':
                try:
                    face = int(parts[1])
                    listener = Listener([face, chat])
                    if not FacesTable.exists(face):
                        raise ValueError
                    elif ListenersTable.exists(listener):
                        answer = 'Вы уже и так получаете уведомления про лицо {}'.format(face)
                    else:
                        ListenersTable.insert(listener)
                        answer = 'Теперь Вам будут приходить уведомления про лицо {}.'.format(face)
                except Exception:
                    answer = 'Вы написали некорректный id :('
            elif len(parts) == 1 and parts[0] == '/delete':
                answer = 'После команды /delete нужно написать выданный id.'
            elif len(parts) == 2 and parts[0] == '/delete':
                try:
                    face = int(parts[1])
                    listener = Listener([face, chat])
                    if not FacesTable.exists(face):
                        raise ValueError
                    elif not ListenersTable.exists(listener):
                        answer = 'Вы и так не получаете уведомления про лицо {}'.format(face)
                    else:
                        ListenersTable.delete(listener)
                        answer = 'Теперь Вам не будут приходить уведомления про лицо {}.'.format(face)
                except Exception:
                    answer = 'Вы написали некорректный id :('
            else:
                answer = 'Я Вас не понимаю, отправьте /help для получения помощи.'
            Bot.bot.send_message(chat, answer)

        Bot.t = threading.Thread(target=Bot.bot.polling)
        Bot.t.start()

    @staticmethod
    def send_message_server(text, face):
        if Config.SEND:
            for chat in ListenersTable.select_by_face(face):
                Bot.bot.send_message(chat.chat, text)
        # else:
        #     print(text)
