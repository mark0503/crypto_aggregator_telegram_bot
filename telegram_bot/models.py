from django.db import models


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    telegram_id = models.CharField(max_length=50)

    def __str__(self):
        return f'Telegram user: {self.first_name} {self.last_name}.'

    class Meta:
        db_table = 'tg_user'
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'
