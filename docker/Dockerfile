FROM python:3.10.0-alpine

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /usr/crypto_aggregator_telegram_bot
VOLUME /usr/crypto_aggregator_telegram_bot

ENV PYTHONPATH /usr/crypto_aggregator_telegram_bot/
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install gunicorn
COPY requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
