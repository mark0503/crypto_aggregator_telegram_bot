from django.core.management.base import BaseCommand

from telegram_bot.utils.telegram_bot import set_webhook_url_for_telegram_bot


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        set_webhook_url_for_telegram_bot()
