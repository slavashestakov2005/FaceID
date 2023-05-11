import requests
from .config import Config


def send_message_client(face, name, result):
    text = Config.MESSAGE_TEMPLATE.format(face, name, result)
    requests.post(Config.MSG_URL, data={'text': text, 'face': face})


def send_parse(face):
    requests.post(Config.PARSE_URL, data={'face': face})
