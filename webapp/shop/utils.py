# utils.py

import requests
from .models import TelegramUser

TELEGRAM_TOKEN = '7810642321:AAGxqRFwFBqRS0hBR9yseX5UpguRKu4sh8k'
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

def send_telegram_message(chat_id, text):
    requests.post(BASE_URL, data={'chat_id': chat_id, 'text': text})

def broadcast_message_to_all(text):
    for user in TelegramUser.objects.all():
        send_telegram_message(user.chat_id, text)
