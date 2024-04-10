import os

import requests

from telegram_bot.models import TelegramUser


def get_telegram_bot_token():
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    return bot_token


def get_telegram_webhook_url():
    telegram_webhook_url = os.environ.get('TELEGRAM_BOT_WEBHOOK_URL')
    return telegram_webhook_url


def get_base_url_for_telegram_bot():
    token = get_telegram_bot_token()
    return f'https://api.telegram.org/bot{token}/'


def set_webhook_url_for_telegram_bot():
    token = get_telegram_bot_token()
    webhook_url = get_telegram_webhook_url()
    requests.get(f'https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}/bot/webhook/')


def get_telegram_user_from_db(user_info: dict) -> TelegramUser:
    user_id = user_info['id']
    old_user = TelegramUser.objects.filter(telegram_id=user_id).first()
    if old_user:
        return old_user
    else:
        first_name = user_info.get('first_name')
        last_name = user_info.get('last_name')
        if last_name is None:
            last_name = first_name
        obj = TelegramUser.objects.create(
            telegram_id=user_id,
            first_name=first_name,
            last_name=last_name
        )
        return obj

