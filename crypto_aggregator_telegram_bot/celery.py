import os

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_aggregator_telegram_bot.settings')

app = Celery(
    'crypto_aggregator_telegram_bot',
    broker='redis://localhost:6379//',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


crypto_aggregator = Exchange('crypto_aggregator')

app.conf.task_queues = (
    Queue('crypto_aggregator', crypto_aggregator),
)

app.conf.task_routes = {
    'parsing.tasks.check_info_on_supplier': {'queue': 'crypto_aggregator'},
    'parsing.tasks.periodical_aggregate_place_task': {'queue': 'crypto_aggregator'}
}

app.conf.beat_schedule = {
    'periodically_aggregate_places': {
        'task': 'parsing.tasks.check_info_on_supplier',
        'schedule': crontab(minute=1),
        'options': {'queue': 'crypto_aggregator'},
    },
}

app.conf.timezone = 'UTC'
