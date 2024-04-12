# Crypto Aggregator && Telegram Bot

## About

This is a Django-based project designed to aggregate cryptocurrency exchanges, 
to store information about price changes of various trading currencies that can be purchased with regular currency. 
There is also a module intended for communication with a Telegram Bot written using webhooks.


## Installation
LOOK .ENV_TEMPLATE
```shell
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data
```

## Run

### Run with docker:
```shell
docker-compose build
docker-compose up
```

### Run without docker:
Run server:
```shell
python manage.py runserver 
```

## Aggregator

Start celery beat process:

```shell
celery -A crypto_aggregator_telegram_bot beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Start celery worker process:
celery -A crypto_aggregator_telegram_bot inspect scheduled
```shell
celery -A crypto_aggregator_telegram_bot -Q crypto_aggregator  # Queue for aggregator
```

To purge tasks from queue do:

```shell
celery -A crypto_aggregator_telegram_bot purge
```


To scrape crypto places:

```python
from parsing.tasks import check_info_on_supplier
check_info_on_supplier.delay()
```

## Telegram Bot

Settings webhook:
```shell
python manage.py set_webhook_telegram_bot
```